"""
WebGearStream 模块 - 封装 WebGear 视频流功能
"""
import asyncio
import threading
import time
import socket
import os
import uvicorn
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
import cv2
from starlette.routing import Route
from starlette.responses import HTMLResponse
import numpy as np
import logging
import sys

# 配置日志
logger = logging.getLogger("aitoolkit_cam.web_stream")

class WebGearStream:
    """
    WebGearStream 类 - 封装 WebGear 视频流功能
    
    该类负责将视频帧通过网络流式传输，支持局域网访问
    """
    
    def __init__(self, source=0, host="localhost", port=8000, reduction=30):
        """
        初始化 WebGearStream
        
        参数:
            source: 视频源，可以是摄像头索引(0,1...)或视频文件路径
            host: 服务器主机地址，使用"0.0.0.0"可从网络访问，"localhost"仅本机访问
            port: 服务器端口号
            reduction: 图像尺寸减少百分比，用于提高性能，设为0则不减少
        """
        self.source = source
        self.host = host
        self.port = port
        self.reduction = reduction
        
        # 自动获取本机IP（如果需要）
        if host == "auto":
            self.host = self._get_local_ip()
        
        # 状态标志
        self.is_running = False
        
        # 获取用户主目录下的数据目录
        data_dir = os.path.join(os.path.expanduser("~"), ".aitoolkit_cam")
        os.makedirs(data_dir, exist_ok=True)
        
        # 创建自定义选项字典，配置简洁的UI
        options = {
            "frame_size_reduction": self.reduction,  # 帧尺寸减少百分比
            "jpeg_compression_quality": 85,  # 设置较高的JPEG质量
            "jpeg_compression_fastdct": True,  # 更快的DCT算法
            "jpeg_compression_fastupsample": False,  # 不使用快速上采样
            "custom_data_location": data_dir  # 使用自定义数据目录
        }
        
        try:
            # 尝试创建WebGear实例 - 不要指定source，稍后在帧生产者设置
            self.web = WebGear(enablePiCamera=False, logging=False, **options)
            
            # 添加自定义路由
            self._setup_clean_ui()
        except Exception as e:
            logger.warning(f"WebGear初始化错误: {e}")
            # 创建一个使用自定义生产者的WebGear实例
            self.web = WebGear(enablePiCamera=False, logging=False, **options)
            
            # 覆盖默认的generator
            self.web.config["generator"] = self._blank_frame_producer
            
            # 添加自定义路由
            self._setup_clean_ui()
        
        # 服务器线程
        self.server_thread = None
        
        # 帧生产者回调
        self.frame_producer_callback = None
    
    def _setup_clean_ui(self):
        """设置一个干净的UI，只显示视频流"""
        # 创建纯净视频界面路由函数
        async def clean_video_page(request):
            # 返回简洁的HTML页面，只包含视频元素
            html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Stream</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
            background-color: #000;
        }
        
        .video-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .video-stream {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        
        /* 添加状态指示器 */
        .status-indicator {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background-color: green;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="video-container">
        <img src="/video" class="video-stream" alt="">
        <div class="status-indicator"></div>
    </div>
    
    <script>
        // 添加错误处理和自动刷新功能
        const img = document.querySelector('.video-stream');
        const statusIndicator = document.querySelector('.status-indicator');
        
        // 图像加载失败处理
        img.onerror = function() {
            statusIndicator.style.backgroundColor = 'red';
            // 3秒后刷新
            setTimeout(() => {
                img.src = '/video?' + new Date().getTime();
            }, 3000);
        };
        
        // 图像加载成功
        img.onload = function() {
            statusIndicator.style.backgroundColor = 'green';
        };
        
        // 保持连接活跃
        setInterval(() => {
            if (!img.complete || img.naturalWidth === 0) {
                img.src = '/video?' + new Date().getTime();
            }
        }, 10000);
    </script>
</body>
</html>"""
            return HTMLResponse(content=html_content)
            
        # 不要完全替换路由，而是添加自定义路由到现有的路由表的前面
        self.web.routes.insert(0, Route("/", endpoint=clean_video_page))
        
        # 确保路由表有效
        if not self.web.routes:
            raise ValueError("WebGear路由表设置失败")
    
    def set_frame_producer(self, callback):
        """
        设置帧生产者回调函数
        
        参数:
            callback: 异步生成器函数，用于生成视频帧
        """
        self.frame_producer_callback = callback
        if callback:
            self.web.config["generator"] = callback
    
    async def _blank_frame_producer(self):
        """生成黑色帧的帧生产者，用于初始化失败时的占位显示"""
        while self.is_running:
            # 创建黑色帧
            blank_frame = self._create_blank_frame(message="等待摄像头连接...")
            
            # 编码为JPEG格式
            _, encoded_img = cv2.imencode('.jpg', blank_frame)
            img_bytes = encoded_img.tobytes()
            
            # 以MultiPart格式返回
            yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
            
            # 短暂延迟
            await asyncio.sleep(0.5)
    
    def _create_blank_frame(self, width=640, height=480, message="等待摄像头连接..."):
        """创建带有文字的空白帧"""
        # 创建黑色背景
        img = np.zeros((height, width, 3), np.uint8)
        
        # 添加文字
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = message
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        
        # 计算文字位置使其居中
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        
        # 写入文字
        cv2.putText(img, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
        
        # 添加当前时间戳，以便查看画面是否更新
        time_text = time.strftime("%H:%M:%S", time.localtime())
        cv2.putText(img, time_text, (10, 30), font, 0.5, (100, 100, 255), 1)
        
        return img
    
    async def default_frame_producer(self):
        """默认帧生产者，如果没有设置自定义的帧生产者，则使用此函数"""
        # 打开视频源
        try:
            cap = cv2.VideoCapture(self.source)
            
            if not cap.isOpened():
                logger.warning(f"无法打开视频源: {self.source}")
                # 改用黑色帧生产者
                async for frame in self._blank_frame_producer():
                    yield frame
                return
            
            try:
                # 循环生成帧
                while self.is_running:
                    # 读取一帧
                    ret, frame = cap.read()
                    
                    # 如果读取失败，使用黑色帧
                    if not ret:
                        blank_frame = self._create_blank_frame(message="读取摄像头失败...")
                        # 编码为JPEG格式
                        _, encoded_img = cv2.imencode('.jpg', blank_frame)
                        img_bytes = encoded_img.tobytes()
                        
                        # 以MultiPart格式返回
                        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
                        
                        # 短暂延迟后继续尝试
                        await asyncio.sleep(0.5)
                        continue
                    
                    # 处理帧
                    if self.reduction > 0:
                        # 缩小图像以提高性能
                        frame = await reducer(frame, percentage=self.reduction, interpolation=cv2.INTER_AREA)
                    
                    # 编码为JPEG格式
                    _, encoded_img = cv2.imencode('.jpg', frame)
                    img_bytes = encoded_img.tobytes()
                    
                    # 以MultiPart格式返回
                    yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
                    
                    # 短暂延迟，避免CPU过载
                    await asyncio.sleep(0.01)
            
            finally:
                # 确保资源释放
                if cap is not None and cap.isOpened():
                    cap.release()
        
        except Exception as e:
            logger.error(f"帧生产者错误: {e}")
            # 出错时使用黑色帧
            async for frame in self._blank_frame_producer():
                yield frame
    
    def _server_thread_function(self):
        """后台线程运行服务器"""
        # 创建事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 启动服务器
        try:
            uvicorn.run(
                self.web(), 
                host=self.host, 
                port=self.port,
                log_level="error"  # 仅显示错误信息，减少日志输出
            )
        except Exception as e:
            logger.error(f"服务器错误: {e}")
        finally:
            if loop.is_running():
                loop.stop()
    
    def _get_local_ip(self):
        """获取本机在局域网中的IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接到公共DNS服务器（不会建立实际连接）
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "localhost"
    
    def _find_available_port(self, start_port=8000, max_attempts=10):
        """查找可用的端口号"""
        for offset in range(max_attempts):
            test_port = start_port + offset
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.host if self.host != "0.0.0.0" else "127.0.0.1", test_port))
                sock.close()
                if result != 0:  # 端口没有被占用
                    return test_port
            except:
                continue
        return start_port  # 如果没找到可用端口，返回原始端口
    
    def start(self):
        """启动网页服务器"""
        if self.is_running:
            return self._get_access_url()
        
        self.is_running = True
        
        # 查找可用端口
        self.port = self._find_available_port(self.port)
        
        # 如果没有设置自定义帧生产者，使用默认帧生产者
        if not self.frame_producer_callback:
            self.set_frame_producer(self.default_frame_producer)
        
        # 启动服务器线程
        self.server_thread = threading.Thread(
            target=self._server_thread_function,
            daemon=True
        )
        self.server_thread.start()
        
        # # 等待服务器启动
        # time.sleep(2)
        
        url = self._get_access_url()
        logger.info(f"Web服务器已启动，访问地址: {url}")
        
        return url
    
    def _get_access_url(self):
        """获取访问URL（支持局域网访问）"""
        # 如果主机是0.0.0.0，返回局域网IP
        display_host = self.host
        if self.host == "0.0.0.0":
            display_host = self._get_local_ip()
        
        return f"http://{display_host}:{self.port}/"
    
    def stop(self):
        """停止服务器"""
        self.is_running = False
        
        # 关闭WebGear
        if hasattr(self, 'web'):
            self.web.shutdown()
        
        logger.info("WebGear服务器已关闭") 