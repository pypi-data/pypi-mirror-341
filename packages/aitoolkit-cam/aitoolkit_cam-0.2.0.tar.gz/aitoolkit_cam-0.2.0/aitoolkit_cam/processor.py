"""
图像处理模块 - 提供图像处理功能
"""
import cv2
import numpy as np
from typing import Optional, Any, Dict, List, Tuple, Union
from .camera import Camera

class Processor:
    """
    图像处理类，提供各种图像效果处理
    
    使用方法:
    ```
    from aitoolkit_cam import Processor
    
    # 创建处理器
    processor = Processor(effect_type="gray")  # 创建灰度处理器
    
    # 处理图像
    gray_image = processor.process(image)
    
    # 切换效果
    processor.set_effect("edge")
    edge_image = processor.process(image)
    
    # 获取当前效果和支持的所有效果
    current_effect = processor.get_effect()
    all_effects = processor.get_supported_effects()
    ```
    """
    
    def __init__(self, effect_type: str = "original"):
        """
        初始化图像处理器
        
        参数:
            effect_type: 效果类型, 可选值包括:
                - "original": 原始图像
                - "gray": 灰度图像
                - "edge": 边缘检测
                - "blur": 高斯模糊
                - "sketch": 素描效果
                - "cartoon": 卡通效果
        """
        self.effect_type = effect_type
        # 支持的效果列表
        self.SUPPORTED_EFFECTS = ["original", "gray", "edge", "blur", "sketch", "cartoon"]
        # 验证效果类型
        if self.effect_type not in self.SUPPORTED_EFFECTS:
            print(f"警告: 不支持的效果类型 '{effect_type}'，已设置为 'original'")
            self.effect_type = "original"

    def set_effect(self, effect_type: str) -> None:
        """
        设置效果类型
        
        参数:
            effect_type: 效果类型
        """
        if effect_type not in self.SUPPORTED_EFFECTS:
            print(f"警告: 不支持的效果类型 '{effect_type}'，保持当前设置")
            return
        self.effect_type = effect_type
    
    def get_effect(self) -> str:
        """
        获取当前效果类型
        
        返回:
            当前效果类型
        """
        return self.effect_type
    
    def get_supported_effects(self) -> List[str]:
        """
        获取所有支持的效果列表
        
        返回:
            支持的效果列表
        """
        return self.SUPPORTED_EFFECTS
    
    def process(self, frame: np.ndarray) -> np.ndarray:
        """
        处理图像帧
        
        参数:
            frame: 输入图像帧
        
        返回:
            处理后的图像帧
        """
        if frame is None:
            return None
        
        # 根据效果类型处理图像
        if self.effect_type == "original":
            return frame
        elif self.effect_type == "gray":
            return self._convert_to_gray(frame)
        elif self.effect_type == "edge":
            return self._detect_edges(frame)
        elif self.effect_type == "blur":
            return self._apply_blur(frame)
        elif self.effect_type == "sketch":
            return self._create_sketch(frame)
        elif self.effect_type == "cartoon":
            return self._create_cartoon(frame)
        else:
            return frame  # 默认返回原始帧

    def _convert_to_gray(self, frame: np.ndarray) -> np.ndarray:
        """将图像转换为灰度"""
        if frame is None:
            return None
            
        try:
            # 检查是否已经是灰度图
            if len(frame.shape) == 2:
                return frame
                
            # 转换为灰度图
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            print(f"灰度转换错误: {e}")
            return frame
    
    def _detect_edges(self, frame: np.ndarray) -> np.ndarray:
        """边缘检测效果"""
        if frame is None:
            return None
            
        try:
            # 如果是彩色图像，先转为灰度
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # 使用Canny算法进行边缘检测
            return cv2.Canny(gray, 50, 150)
        except Exception as e:
            print(f"边缘检测错误: {e}")
            return frame
    
    def _apply_blur(self, frame: np.ndarray) -> np.ndarray:
        """高斯模糊效果"""
        if frame is None:
            return None
            
        try:
            return cv2.GaussianBlur(frame, (15, 15), 0)
        except Exception as e:
            print(f"高斯模糊错误: {e}")
            return frame
    
    def _create_sketch(self, frame: np.ndarray) -> np.ndarray:
        """素描效果"""
        if frame is None:
            return None
            
        try:
            # 如果是彩色图像，先转为灰度
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
            
            # 对灰度图像进行高斯模糊
            inv = 255 - gray
            blur = cv2.GaussianBlur(inv, (21, 21), 0)
            
            # 叠加模糊图像和灰度图像，模拟素描效果
            return cv2.divide(gray, 255 - blur, scale=256)
        except Exception as e:
            print(f"素描效果错误: {e}")
            return frame
    
    def _create_cartoon(self, frame: np.ndarray) -> np.ndarray:
        """卡通效果"""
        if frame is None:
            return None
            
        try:
            # 降噪处理
            color = cv2.bilateralFilter(frame, 9, 300, 300)
            
            # 边缘检测
            if len(frame.shape) == 3:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                gray = frame
                color = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            # 使用自适应阈值处理
            edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY, 9, 3)
            
            # 如果是灰度图，则转回彩色图以便合并
            if len(frame.shape) == 2:
                edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
            
            # 合并边缘和颜色图像
            return cv2.bitwise_and(color, color, mask=edge)
        except Exception as e:
            print(f"卡通效果错误: {e}")
            return frame


def apply_effect(frame: np.ndarray, effect_type: str, **kwargs) -> np.ndarray:
    """
    对图像应用指定效果
    
    参数:
        frame: 输入图像帧
        effect_type: 效果类型
        **kwargs: 附加参数，依效果类型而定
    
    返回:
        处理后的图像帧
        
    示例:
    ```python
    import cv2
    from aitoolkit_cam import apply_effect
    
    # 读取图像
    image = cv2.imread('image.jpg')
    
    # 应用不同效果
    gray = apply_effect(image, 'gray')
    edge = apply_effect(image, 'edge', threshold1=100, threshold2=200)
    blur = apply_effect(image, 'blur', ksize=(21, 21))
    sketch = apply_effect(image, 'sketch')
    cartoon = apply_effect(image, 'cartoon')
    
    # 显示结果
    cv2.imshow('原图', image)
    cv2.imshow('灰度', gray)
    cv2.imshow('边缘', edge)
    cv2.imshow('模糊', blur)
    cv2.imshow('素描', sketch)
    cv2.imshow('卡通', cartoon)
    cv2.waitKey(0)
    ```
    """
    # 创建临时处理器
    processor = Processor(effect_type)
    # 处理并返回
    return processor.process(frame)


class ProcessedCamera(Camera):
    """
    具有实时图像处理效果的摄像头类
    
    在标准Camera类的基础上添加了图像处理功能
    
    使用方法:
    ```python
    from aitoolkit_cam import ProcessedCamera
    
    # 创建带有图像处理效果的摄像头对象
    cam = ProcessedCamera(source=0, effect_type="sketch")
    
    # 启动网页服务器
    url = cam.start()
    print(f"请访问: {url}")
    
    # 迭代获取处理后的帧
    for frame in cam:
        # frame已经应用了指定效果
        pass
    
    # 随时切换效果
    cam.set_effect("cartoon")
    
    # 关闭资源
    cam.stop()
    ```
    """
    
    def __init__(self, source=0, host="localhost", port=8000, reduction=30, 
                 effect_type="original", effect_params=None, **kwargs):
        """
        初始化具有图像处理效果的摄像头
        
        参数:
            source: 视频源，可以是摄像头索引(0,1...)或视频文件路径
            host: 服务器主机地址，使用"0.0.0.0"可从网络访问，"localhost"仅本机访问
            port: 服务器端口号
            reduction: 图像尺寸减少百分比，用于提高性能，设为0则不减少
            effect_type: 效果类型，可选值包括"original", "gray", "edge", "blur", "sketch", "cartoon"
            effect_params: 效果参数，根据effect_type不同而变化
            **kwargs: 其他传递给Camera初始化的参数
        """
        # 初始化基类
        super().__init__(source, host, port, reduction, **kwargs)
        
        # 创建图像处理器
        self.processor = Processor(effect_type)
        
        # 存储效果参数
        self.effect_params = effect_params or {}
    
    def set_effect(self, effect_type):
        """
        设置图像处理效果
        
        参数:
            effect_type: 效果类型
        """
        self.processor.set_effect(effect_type)
    
    def get_effect(self):
        """
        获取当前效果类型
        
        返回:
            当前效果类型
        """
        return self.processor.get_effect()
    
    def get_supported_effects(self):
        """
        获取所有支持的效果列表
        
        返回:
            支持的效果列表
        """
        return self.processor.get_supported_effects()
    
    def __iter__(self):
        """
        重写迭代器方法，返回处理后的帧
        """
        # 使用基类的迭代器
        self._iterator = super().__iter__()
        return self
    
    def __next__(self):
        """
        获取下一帧并应用当前效果
        
        返回:
            处理后的帧
        """
        # 获取原始帧
        frame = next(self._iterator)
        
        # 应用效果处理
        processed_frame = self.processor.process(frame)
        
        # 在网页端显示处理后的帧
        self.set_current_frame(processed_frame)
        
        return processed_frame 