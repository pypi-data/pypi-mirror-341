"""
AIToolkit Camera - 简单易用的摄像头工具包
===========================================

提供本地显示和网页显示功能，支持各种图像处理效果
"""

# 从core模块导入所有公开的类和函数
from .core import Camera, ProcessedCamera, apply_effect, cv_show

# 指定公开的API
__all__ = ['Camera', 'ProcessedCamera', 'apply_effect', 'cv_show']

# 版本信息
__version__ = '0.1.0' 