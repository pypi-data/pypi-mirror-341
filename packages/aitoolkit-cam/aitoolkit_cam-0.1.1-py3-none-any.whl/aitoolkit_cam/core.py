"""
AIToolkit Camera 核心模块 - 提供摄像头类和图像处理功能
"""
from typing import Any, Dict, Iterator
import cv2
import asyncio
import threading
import time
import socket
import os
import uvicorn
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
from starlette.templating import Jinja2Templates
from starlette.routing import Route
from starlette.responses import HTMLResponse

# 全局图像处理函数
def apply_effect(frame, effect_type="original", **kwargs):
    """
    应用各种图像处理效果到帧
    
    参数:
        frame: 输入图像
        effect_type: 效果类型，可选值：
            - "original": 原始图像
            - "gray": 灰度图
            - "edge": 边缘检测
            - "blur": 高斯模糊
            - "sketch": 素描效果
            - "cartoon": 卡通效果
        **kwargs: 其他效果参数
    
    返回:
        处理后的图像
    """
    if frame is None:
        return None
    
    # 创建原始帧的副本
    result = frame.copy()
    
    if effect_type == "original":
        return result
    
    elif effect_type == "gray":
        return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    
    elif effect_type == "edge":
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        return cv2.Canny(blurred, 
                         kwargs.get("threshold1", 30), 
                         kwargs.get("threshold2", 100))
    
    elif effect_type == "blur":
        ksize = kwargs.get("ksize", 15)
        return cv2.GaussianBlur(result, (ksize, ksize), 0)
    
    elif effect_type == "sketch":
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        inv = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inv, (21, 21), 0)
        inv_blurred = cv2.bitwise_not(blurred)
        return cv2.divide(gray, inv_blurred, scale=256.0)
    
    elif effect_type == "cartoon":
        # 边缘检测
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        blurred = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            blurred, 
            255, 
            cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY, 
            9, 
            9
        )
        
        # 颜色量化
        color = cv2.bilateralFilter(result, 9, 300, 300)
        
        # 组合边缘和量化结果
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon
    
    else:
        print(f"未知效果类型: {effect_type}")
        return result


def cv_show(frame, mode="cv2", window_name="Preview", wait_key=1):
    """
    显示图像，支持cv2和web两种模式
    
    参数:
        frame: 要显示的图像
        mode: 显示模式，"cv2"或"web"
        window_name: 窗口名称
        wait_key: cv2.waitKey的等待时间
    
    返回:
        如果按下'q'则返回True，否则返回False
    """
    if frame is None:
        return False
    
    if mode.lower() == "cv2":
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(wait_key) & 0xFF
        if key == ord('q'):
            return True
    elif mode.lower() == "web":
        # Web模式不做任何事情，因为Camera类已经处理了web显示
        pass
    else:
        print(f"未知显示模式: {mode}")
    
    return False


class Camera:
    """
    摄像头类，使用WebGear在浏览器中显示视频流
    支持迭代器协议，可以使用for循环获取帧
    
    使用方法:
    ```
    # 创建实例
    cam = Camera(source=0)
    
    # 1. 迭代器用法
    for frame in cam:
        cv_show(frame, "cv2")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 2. 浏览器显示
    url = cam.start()
    print(f"请访问: {url}")
    
    # 3. 本地窗口显示
    cam.show_local()
    
    # 停止
    cam.stop()
    ```
    """
    
    def __init__(self, source=0, host="localhost", port=8000, reduction=30):
        """
        初始化Camera
        
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
        self.local_display = False
        
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
        
        # 创建WebGear实例 - 禁用日志输出
        self.web = WebGear(source=self.source, logging=False, **options)
        
        # 添加自定义路由 - 修复后的方式
        self._setup_clean_ui()
        
        # 设置自定义帧生产者
        self.web.config["generator"] = self._frame_producer
        
        # 服务器线程
        self.server_thread = None
        
        # 本地显示线程
        self.local_thread = None
        
        # 共享的视频捕获对象
        self.cap = None
        self.frame = None
        self.frame_ready = False
        self.frame_lock = threading.Lock()
        
        # 迭代器变量
        self._iterator_cap = None
    
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
    </style>
</head>
<body>
    <div class="video-container">
        <img src="/video" class="video-stream" alt="">
    </div>
</body>
</html>"""
            return HTMLResponse(content=html_content)
            
        # 不要完全替换路由，而是添加自定义路由到现有的路由表的前面
        self.web.routes.insert(0, Route("/", endpoint=clean_video_page))
        
        # 确保路由表有效
        if not self.web.routes:
            raise ValueError("WebGear路由表设置失败")
    
    def __iter__(self) -> Iterator[Any]:
        """
        返回迭代器对象，支持for frame in cam语法
        """
        # 如果已经有WebGear在运行，共用它的帧
        if self.is_running and self.cap is not None:
            return self
        
        # 否则，创建一个新的视频捕获对象
        self._iterator_cap = cv2.VideoCapture(self.source)
        if not self._iterator_cap.isOpened():
            raise RuntimeError(f"无法打开视频源: {self.source}")
        
        return self
    
    def __next__(self) -> Any:
        """
        迭代器的next方法，获取下一帧
        """
        # 如果WebGear在运行，使用共享的帧
        if self.is_running and self.cap is not None:
            # 等待帧就绪
            while not self.frame_ready and self.is_running:
                time.sleep(0.01)
            
            with self.frame_lock:
                if not self.frame_ready:
                    raise StopIteration
                frame = self.frame.copy()
            
            return frame
        
        # 否则，使用迭代器专用的捕获对象
        if self._iterator_cap is None or not self._iterator_cap.isOpened():
            raise StopIteration
        
        ret, frame = self._iterator_cap.read()
        if not ret:
            self._close_iterator()
            raise StopIteration
        
        return frame
    
    def _close_iterator(self):
        """关闭迭代器的资源"""
        if self._iterator_cap is not None:
            self._iterator_cap.release()
            self._iterator_cap = None
    
    async def _frame_producer(self):
        """自定义帧生产者，为WebGear提供视频帧"""
        # 打开视频源
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            print(f"无法打开视频源: {self.source}")
            return
        
        # 保存视频捕获对象以便其他线程使用
        self.cap = cap
        
        try:
            # 循环生成帧
            while self.is_running:
                # 读取一帧
                ret, frame = cap.read()
                
                # 如果读取失败，退出循环
                if not ret:
                    break
                
                # 保存当前帧，用于本地显示和迭代器
                with self.frame_lock:
                    self.frame = frame.copy()
                    self.frame_ready = True
                
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
            if self.cap is not None:
                self.cap.release()
                self.cap = None
    
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
            print(f"服务器错误: {e}")
        finally:
            if loop.is_running():
                loop.stop()
    
    def _local_display_thread(self):
        """本地显示线程"""
        window_name = "本地摄像头预览"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        last_time = time.time()
        frame_count = 0
        fps = 0
        
        while self.local_display and self.is_running:
            # 获取当前帧
            frame_available = False
            current_frame = None
            
            with self.frame_lock:
                if self.frame_ready:
                    current_frame = self.frame.copy()
                    frame_available = True
            
            # 显示帧
            if frame_available:
                # 计算帧率
                frame_count += 1
                current_time = time.time()
                elapsed = current_time - last_time
                
                if elapsed >= 1.0:
                    fps = frame_count / elapsed
                    frame_count = 0
                    last_time = current_time
                
                # 添加FPS信息
                cv2.putText(
                    current_frame,
                    f"FPS: {fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )
                
                # 显示
                cv2.imshow(window_name, current_frame)
                
                # 处理按键
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.local_display = False
                    break
            
            # 短暂延迟
            time.sleep(0.01)
        
        cv2.destroyWindow(window_name)
    
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
    
    def start(self):
        """启动摄像头网页服务器"""
        if self.is_running:
            return self._get_access_url()
        
        self.is_running = True
        
        # 启动服务器线程
        self.server_thread = threading.Thread(
            target=self._server_thread_function,
            daemon=True
        )
        self.server_thread.start()
        
        # 等待服务器启动
        time.sleep(2)
        
        url = self._get_access_url()
        print(f"访问地址: {url}")
        
        return url
    
    def _get_access_url(self):
        """获取访问URL（支持局域网访问）"""
        # 如果主机是0.0.0.0，返回局域网IP
        display_host = self.host
        if self.host == "0.0.0.0":
            display_host = self._get_local_ip()
        
        return f"http://{display_host}:{self.port}/"
    
    def show_local(self):
        """在本地窗口中显示视频流（非阻塞）"""
        if not self.is_running:
            self.start()
        
        if self.local_display:
            return
        
        self.local_display = True
        
        # 启动本地显示线程
        self.local_thread = threading.Thread(
            target=self._local_display_thread,
            daemon=True
        )
        self.local_thread.start()
        
        print("本地预览已启动 (按'q'键退出)")
    
    def wait_for_exit(self):
        """等待用户按Enter键退出"""
        print("按Enter键退出...")
        input()
        self.stop()
    
    def stop(self):
        """停止摄像头和服务器"""
        self.is_running = False
        self.local_display = False
        
        # 关闭WebGear
        if hasattr(self, 'web'):
            self.web.shutdown()
        
        # 关闭视频捕获
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        # 关闭迭代器资源
        self._close_iterator()
        
        print("摄像头已关闭")


class ProcessedCamera(Camera):
    """
    带图像处理效果的摄像头类
    继承自Camera，增加了图像处理功能
    
    使用方法与Camera相同，但增加了效果选择功能
    """
    
    def __init__(self, source=0, host="localhost", port=8000, reduction=30, 
                 effect_type="original", **effect_params):
        """
        初始化ProcessedCamera
        
        参数:
            source: 视频源，可以是摄像头索引(0,1...)或视频文件路径
            host: 服务器主机地址，使用"0.0.0.0"可从网络访问，"localhost"仅本机访问
            port: 服务器端口号
            reduction: 图像尺寸减少百分比，用于提高性能，设为0则不减少
            effect_type: 图像处理效果类型
            **effect_params: 效果参数
        """
        super().__init__(source, host, port, reduction)
        self.effect_type = effect_type
        self.effect_params = effect_params
    
    async def _frame_producer(self):
        """重写帧生产者，添加图像处理功能"""
        # 打开视频源
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            print(f"无法打开视频源: {self.source}")
            return
        
        # 保存视频捕获对象以便其他线程使用
        self.cap = cap
        
        try:
            # 循环生成帧
            while self.is_running:
                # 读取一帧
                ret, frame = cap.read()
                
                # 如果读取失败，退出循环
                if not ret:
                    break
                
                # 应用效果
                processed_frame = apply_effect(
                    frame, 
                    self.effect_type, 
                    **self.effect_params
                )
                
                # 保存处理后的帧，用于本地显示
                with self.frame_lock:
                    self.frame = processed_frame.copy()
                    self.frame_ready = True
                
                # 处理帧
                if self.reduction > 0:
                    # 缩小图像以提高性能
                    processed_frame = await reducer(
                        processed_frame, 
                        percentage=self.reduction, 
                        interpolation=cv2.INTER_AREA
                    )
                
                # 确保处理后的帧是3通道的（适用于网页显示）
                if len(processed_frame.shape) == 2:  # 如果是灰度图
                    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
                
                # 编码为JPEG格式
                _, encoded_img = cv2.imencode('.jpg', processed_frame)
                img_bytes = encoded_img.tobytes()
                
                # 以MultiPart格式返回
                yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
                
                # 短暂延迟，避免CPU过载
                await asyncio.sleep(0.01)
        
        finally:
            # 确保资源释放
            if self.cap is not None:
                self.cap.release()
                self.cap = None
    
    def __next__(self):
        """重写迭代器的next方法，添加图像处理功能"""
        # 获取原始帧
        frame = super().__next__()
        
        # 应用效果
        processed_frame = apply_effect(
            frame, 
            self.effect_type, 
            **self.effect_params
        )
        
        return processed_frame
    
    def set_effect(self, effect_type, **effect_params):
        """设置图像处理效果"""
        self.effect_type = effect_type
        self.effect_params = effect_params 