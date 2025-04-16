"""
Camera 模块 - 提供摄像头类
"""
import threading
import time
import cv2
import asyncio
from typing import Any, Iterator
from .web_stream import WebGearStream
import numpy as np

class Camera:
    """
    摄像头类，使用WebGearStream在浏览器中显示视频流
    支持迭代器协议，可以使用for循环获取帧
    
    使用方法:
    ```
    # 创建摄像头对象并启动网页服务
    cam = Camera(0, host="0.0.0.0", port=8000)
    url = cam.start()
    print(f"请在局域网内通过浏览器访问: {url}")
    
    # 迭代获取帧
    for frame in cam:
        # 处理帧并显示（本地或网页）
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cam.cv_show(gray, "web")  # 在网页上显示
        if cam.cv_show(gray, "cv2"):  # 在本地显示
            break
    
    # 关闭摄像头和服务器
    cam.stop()
    ```
    """
    
    def __init__(self, source=0, host="localhost", port=8000, reduction=30, max_failures=10, display_gray=False):
        """
        初始化Camera
        
        参数:
            source: 视频源，可以是摄像头索引(0,1...)或视频文件路径
            host: 服务器主机地址，使用"0.0.0.0"可从网络访问，"localhost"仅本机访问
            port: 服务器端口号
            reduction: 图像尺寸减少百分比，用于提高性能，设为0则不减少
            max_failures: 最大连续失败次数，超过此值会尝试重新打开摄像头
            display_gray: 是否在网页端显示灰度图像
        """
        self.source = source
        self.host = host
        self.port = port
        self.reduction = reduction
        self.max_failures = max_failures
        self.display_gray = display_gray
        
        # 状态标志
        self.is_running = False
        self.stream_running = False
        
        # 创建WebGearStream实例
        self.web_stream = self._create_web_stream()
        
        # 共享的视频捕获对象
        self.cap = None
        # 存储原始帧
        self.frame = None
        # 存储用于网页显示的帧（可能是经过处理的）
        self.web_frame = None
        self.frame_lock = threading.Lock()
        self.frame_ready = False
        
        # 备用帧，用于在获取新帧失败时使用
        self.backup_frame = None
        
        # 独立迭代器的视频捕获对象
        self._iterator_cap = None
        
        # 用于监控和重启WebGearStream的线程
        self.monitor_thread = None
        self.monitor_event = threading.Event()
    
    def _create_web_stream(self):
        """创建一个新的WebGearStream实例"""
        web_stream = WebGearStream(source=self.source, host=self.host, 
                                   port=self.port, reduction=self.reduction)
        # 设置WebGear的帧生产者
        web_stream.set_frame_producer(self._frame_producer)
        return web_stream
    
    def _monitor_web_stream(self):
        """监控WebGearStream状态，在需要时重新启动"""
        while self.is_running and not self.monitor_event.is_set():
            # 检查WebGearStream是否活动
            if self.stream_running and (not hasattr(self.web_stream, 'server_thread') or 
                                       not self.web_stream.server_thread.is_alive()):
                print("检测到WebGear服务器已关闭，正在尝试重新启动...")
                
                try:
                    # 创建新的WebGearStream实例
                    self.web_stream = self._create_web_stream()
                    # 重新启动
                    url = self.web_stream.start()
                    print(f"WebGear服务器已重新启动，访问地址: {url}")
                    self.stream_running = True
                except Exception as e:
                    print(f"重新启动WebGear服务器失败: {e}")
                    self.stream_running = False
                    time.sleep(5)  # 失败后等待一段时间再尝试
                    continue
            
            time.sleep(2)  # 每2秒检查一次
    
    def cv_show(self, frame, mode="cv2", wait_key=1, window_name="预览"):
        """
        显示图像并处理按键
        
        根据模式参数在本地或网页上显示图像。
        
        参数:
            frame: 要显示的图像帧
            mode: 显示模式，"cv2"表示本地显示，"web"表示网页显示
            wait_key: cv2.waitKey的等待时间，单位为毫秒（仅在cv2模式下有效）
            window_name: 窗口名称（仅在cv2模式下有效）
        
        返回:
            如果按下'q'则返回True，否则返回False
        """
        if frame is None:
            return False
        
        # 根据模式决定显示方式
        if mode.lower() == "web":
            # 网页显示
            self.set_current_frame(frame)
            return False  # 网页模式下不检测按键
        else:
            # 本地显示（默认cv2模式）
            # 如果是灰度图，先转回BGR以便显示
            display_frame = frame
            if len(frame.shape) == 2:
                display_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                
            # 显示图像
            cv2.imshow(window_name, display_frame)
            
            # 等待按键并检查是否按下q键
            key = cv2.waitKey(wait_key) & 0xFF
            return key == ord('q')
    
    async def _frame_producer(self):
        """为WebGearStream提供帧"""
        # 打开视频源
        cap = self._open_video_source()
        if cap is None:
            return
        
        # 保存视频捕获对象
        self.cap = cap
        
        failures = 0  # 连续失败计数
        reopened = False  # 是否最近重新打开过摄像头
        blank_image = None  # 备用空白图像
        
        try:
            # 循环生成帧
            while self.is_running:
                # 读取一帧
                ret, frame = cap.read()
                
                # 如果读取失败
                if not ret:
                    failures += 1
                    if failures % 5 == 1:  # 每5次失败只打印一次日志
                        print(f"读取帧失败 ({failures}/{self.max_failures})")
                    
                    # 失败次数过多，尝试重新打开摄像头
                    if failures >= self.max_failures and not reopened:
                        print("尝试重新打开摄像头...")
                        try:
                            # 关闭当前摄像头
                            if self.cap is not None:
                                self.cap.release()
                                
                            # 适当等待以防止立即重连
                            await asyncio.sleep(1.0)
                            
                            # 重新打开
                            new_cap = self._open_video_source()
                            if new_cap is not None:
                                cap = new_cap
                                self.cap = cap
                                failures = 0  # 重置失败计数
                                reopened = True  # 标记最近重新打开过
                                print("摄像头重新打开成功")
                            else:
                                print("重新打开摄像头失败")
                        except Exception as e:
                            print(f"重新打开摄像头出错: {e}")
                    
                    # 使用备用帧或空白图像
                    if self.backup_frame is not None:
                        frame = self.backup_frame.copy()
                    elif blank_image is not None:
                        frame = blank_image.copy()
                    else:
                        # 创建一个空白图像，显示"正在重连..."
                        blank_image = self._create_blank_frame()
                        frame = blank_image
                        
                    # 短暂等待后继续尝试
                    await asyncio.sleep(0.2)
                else:
                    # 读取成功，重置状态
                    failures = 0
                    reopened = False
                    # 保存成功的帧作为备用
                    self.backup_frame = frame.copy()
                
                # 保存原始帧，用于迭代器
                with self.frame_lock:
                    self.frame = frame.copy()
                    self.frame_ready = True
                    
                    # 如果设置了显示灰度图，或者有已经设置的web_frame，则使用它
                    if self.web_frame is not None:
                        # 优先使用自定义的web_frame
                        web_display_frame = self.web_frame.copy()
                    elif self.display_gray:
                        # 否则根据设置转为灰度
                        web_display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        # 灰度图转回BGR以便JPEG编码
                        web_display_frame = cv2.cvtColor(web_display_frame, cv2.COLOR_GRAY2BGR)
                    else:
                        # 否则使用原始帧
                        web_display_frame = frame.copy()
                
                # 编码为JPEG格式
                try:
                    _, jpeg = cv2.imencode('.jpg', web_display_frame)
                    img_bytes = jpeg.tobytes()
                except Exception as e:
                    print(f"编码错误: {e}")
                    await asyncio.sleep(0.1)
                    continue
                
                # 返回多部分格式的图像
                yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
                
                # 短暂延迟，避免CPU过载
                await asyncio.sleep(0.01)
        
        finally:
            # 确保资源释放
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            # 清理状态
            with self.frame_lock:
                self.frame_ready = False
                self.frame = None
                self.web_frame = None
                self.backup_frame = None
    
    def set_current_frame(self, frame):
        """
        设置当前用于网页显示的帧
        
        参数:
            frame: 要显示的图像帧
            
        返回:
            无
            
        注意:
            这个方法允许外部函数更新网页端显示的内容
            传入的帧将替代摄像头捕获的原始帧，直到下一次调用
        """
        if frame is None:
            return
            
        with self.frame_lock:
            # 确保是BGR格式（如果是灰度图，转为BGR）
            if len(frame.shape) == 2:
                self.web_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            else:
                self.web_frame = frame.copy()
    
    def set_display_gray(self, display_gray):
        """
        设置是否在网页端显示灰度图像
        
        参数:
            display_gray: 布尔值，True为显示灰度图，False为显示彩色图
        """
        self.display_gray = display_gray
        
        # 清除之前设置的自定义帧
        with self.frame_lock:
            self.web_frame = None
    
    def _open_video_source(self):
        """打开视频源并返回捕获对象，如果失败返回None"""
        try:
            cap = cv2.VideoCapture(self.source)
            if not cap.isOpened():
                print(f"无法打开视频源: {self.source}")
                return None
            return cap
        except Exception as e:
            print(f"打开视频源时出错: {e}")
            return None
    
    def _create_blank_frame(self, width=640, height=480):
        """创建一个带有文字的空白帧"""
        # 创建黑色背景
        img = np.zeros((height, width, 3), np.uint8)
        
        # 添加文字
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "摄像头连接中..."
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        
        # 计算文字位置使其居中
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        
        # 写入文字
        cv2.putText(img, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
        
        return img
                
    def __iter__(self) -> Iterator[Any]:
        """返回迭代器对象，支持for frame in cam语法"""
        if self.is_running and self.cap is not None:
            # 使用网页服务中的摄像头
            return self
        else:
            # 创建新的独立视频捕获
            self._iterator_cap = self._open_video_source()
            if self._iterator_cap is None:
                raise RuntimeError(f"无法打开视频源: {self.source}")
            return self
    
    def __next__(self) -> Any:
        """迭代器的next方法，获取下一帧"""
        # Web服务正在运行，使用共享摄像头
        if self.is_running and self.cap is not None:
            # 等待帧就绪
            wait_start = time.time()
            while not self.frame_ready and self.is_running:
                time.sleep(0.001)
                if time.time() - wait_start > 5:  # 5秒超时
                    raise StopIteration
            
            # 返回帧
            with self.frame_lock:
                if not self.frame_ready or self.frame is None:
                    raise StopIteration
                return self.frame.copy()
        
        # 使用独立捕获
        elif self._iterator_cap is not None:
            ret, frame = self._iterator_cap.read()
            if not ret:
                self._close_iterator()
                raise StopIteration
            return frame
        
        # 无效状态
        else:
            raise StopIteration
    
    def _close_iterator(self):
        """关闭独立迭代器资源"""
        if self._iterator_cap is not None:
            self._iterator_cap.release()
            self._iterator_cap = None
    
    def start(self):
        """启动摄像头网页服务器"""
        if self.is_running:
            return self.web_stream._get_access_url()
        
        # 确保迭代器资源被释放
        self._close_iterator()
        
        # 设置状态标志
        self.is_running = True
        
        # 启动WebGearStream
        url = self.web_stream.start()
        self.stream_running = True
        
        # 启动监控线程
        self.monitor_event.clear()
        self.monitor_thread = threading.Thread(
            target=self._monitor_web_stream,
            daemon=True
        )
        self.monitor_thread.start()
        
        return url
    
    def stop(self):
        """停止摄像头和服务器"""
        # 先设置标志，让所有循环退出
        self.is_running = False
        self.stream_running = False
        
        # 停止监控线程
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_event.set()
            self.monitor_thread.join(timeout=1.0)
        
        # 停止Web服务
        if hasattr(self, 'web_stream'):
            try:
                self.web_stream.stop()
            except Exception as e:
                print(f"停止WebGear服务器时出错: {e}")
        
        # 关闭独立迭代器资源
        self._close_iterator()
        
        # 短暂延迟确保资源正常释放
        time.sleep(0.1)
        
        print("摄像头和Web服务已关闭") 