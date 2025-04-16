"""
Camera 模块 - 提供简洁的摄像头接口
"""
import threading
import time
import cv2
import asyncio
import numpy as np
import logging
import sys
from .web_stream import WebGearStream

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("aitoolkit_cam")

class Camera:
    """摄像头类，实现迭代器接口和显示功能"""

    def __init__(self, source=0, width=640, height=480, fps=None, web_enabled=False, port=8000):
        """
        初始化摄像头
        
        参数:
            source: 视频源，可以是摄像头索引或视频文件路径
            width: 输出视频帧宽度
            height: 输出视频帧高度
            fps: 摄像头帧率，None表示使用默认值
            web_enabled: 是否启用网页流服务
            port: 网页服务端口号(默认8000)
        """
        # 基本参数
        self.source = source
        self.width = width
        self.height = height
        self.fps = fps
        
        # Web流相关
        self.web_enabled = web_enabled
        self.port = port
        self.web_stream = None
        
        # 状态变量
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.frame_ready = False
        
        # 资源保护
        self._lock = threading.RLock()
        
    def start(self):
        """启动摄像头"""
        if self.is_running:
            logger.info("摄像头已经在运行中")
            return True
            
        # 打开视频源
        try:
            self.cap = cv2.VideoCapture(self.source)
            
            if not self.cap.isOpened():
                logger.error(f"无法打开视频源: {self.source}")
                return False
                
            # 设置分辨率和帧率
            if self.width and self.height:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                
            if self.fps is not None:
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                
            # 获取实际设置的属性
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"摄像头已设置为: {actual_width}x{actual_height} @ {actual_fps}fps")
            
            # 启动Web服务（如果需要）
            if self.web_enabled:
                self._start_web_stream()
            
            self.is_running = True
            return True
            
        except Exception as e:
            logger.error(f"启动摄像头失败: {e}")
            if self.cap:
                self.cap.release()
                self.cap = None
            return False
    
    def _start_web_stream(self):
        """启动Web流服务"""
        try:
            # 创建WebGearStream实例
            self.web_stream = WebGearStream(
                source=self.source,
                host="0.0.0.0",  # 允许从网络访问
                port=self.port
            )
            
            # 定义帧生产者函数
            async def frame_producer():
                while self.is_running:
                    try:
                        # 获取当前帧
                        with self._lock:
                            frame = self.current_frame.copy() if self.frame_ready and self.current_frame is not None else None
                            
                        if frame is None:
                            await asyncio.sleep(0.1)
                            continue
                        
                        # 编码为JPEG
                        _, buffer = cv2.imencode('.jpg', frame)
                        frame_bytes = buffer.tobytes()
                        
                        # 生成MJPEG帧
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                        
                    except Exception as e:
                        logger.error(f"生成MJPEG流时出错: {e}")
                        await asyncio.sleep(0.1)
            
            # 设置帧生产者并启动服务
            self.web_stream.set_frame_producer(frame_producer)
            url = self.web_stream.start()
            logger.info(f"Web流服务已启动: {url}")
            
            return url
        except Exception as e:
            logger.error(f"启动Web流服务失败: {e}")
            return None
    
    def stop(self):
        """停止摄像头并释放资源"""
        if not self.is_running:
            return
            
        logger.info("停止摄像头...")
        
        # 更新状态
        self.is_running = False
        
        # 停止Web流服务
        if self.web_stream:
            try:
                self.web_stream.stop()
                logger.info("Web流服务已停止")
            except Exception as e:
                logger.error(f"停止Web流服务时出错: {e}")
            finally:
                self.web_stream = None
        
        # 释放摄像头资源
        if self.cap:
            self.cap.release()
            self.cap = None
            
        # 重置状态
        with self._lock:
            self.current_frame = None
            self.frame_ready = False
            
        logger.info("摄像头已停止")
        
    def get_web_url(self):
        """获取网页流服务的访问URL"""
        if not self.web_stream:
            return None
            
        try:
            return self.web_stream._get_access_url()
        except Exception as e:
            logger.error(f"获取Web流URL时出错: {e}")
            return None
    
    def cv_show(self, frame, mode="cv2", wait_key=1, window_name="预览"):
        """
        显示图像并处理按键
        
        参数:
            frame: 要显示的图像帧
            mode: 显示模式，"cv2"表示本地显示，"web"表示网页显示
            wait_key: cv2.waitKey的等待时间(毫秒)，仅cv2模式有效
            window_name: 窗口名称，仅cv2模式有效
        
        返回:
            cv2模式下，如果按下'q'或'ESC'则返回True
            web模式下，总是返回False
        """
        if frame is None:
            return False
        
        # 根据模式决定显示方式
        if mode.lower() == "web":
            # 网页显示(更新当前帧)
            with self._lock:
                self.current_frame = frame.copy()
                self.frame_ready = True
            return False
        else:
            # 本地显示
            # 如果是灰度图，转换回BGR以便显示
            if len(frame.shape) == 2:
                display_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            else:
                display_frame = frame
                
            # 显示图像
            cv2.imshow(window_name, display_frame)
            
            # 等待按键并检查是否按下q键或ESC键
            key = cv2.waitKey(wait_key) & 0xFF
            return key == ord('q') or key == 27  # 27是ESC键的ASCII码
    
    def read(self):
        """
        读取一帧（OpenCV兼容接口）
        
        返回:
            (ret, frame) 元组，ret表示是否成功，frame为读取的帧
        """
        if not self.is_running or not self.cap:
            return False, None
            
        try:
            with self._lock:
                ret, frame = self.cap.read()
                
                if ret:
                    self.current_frame = frame.copy()
                    self.frame_ready = True
                    
                return ret, frame
        except Exception as e:
            logger.error(f"读取帧出错: {e}")
            return False, None
    
    def __iter__(self):
        """返回迭代器自身"""
        if not self.is_running:
            self.start()
        return self
    
    def __next__(self):
        """获取下一帧"""
        if not self.is_running:
            raise StopIteration
            
        ret, frame = self.read()
        if not ret:
            raise StopIteration
            
        return frame
    
    def __enter__(self):
        """上下文管理器入口"""
        if not self.is_running:
            self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
        
    def __del__(self):
        """析构函数，确保资源释放"""
        self.stop() 