"""
AIToolkit Camera - 简单易用的摄像头工具包
===========================================

提供本地显示和网页显示功能，支持图像处理

此包提供了使用OpenCV的摄像头工具，它具有以下特点：
1. 简单的API，易于使用
2. 支持本地窗口显示和网页浏览器显示
3. 提供多种图像处理效果
4. 兼容迭代器协议，可用于for循环
5. 自动处理摄像头连接和断开

快速示例:
```python
from aitoolkit_cam import Camera

# 创建摄像头对象
cam = Camera(0)

# 启动网页服务器
url = cam.start()
print(f"请访问: {url}")

# 在网页模式下显示
for frame in cam:
    # 可以进行额外的处理
    pass

try:
    cam.wait_for_exit()
except KeyboardInterrupt:
    pass

# 释放资源
cam.stop()
```
"""

# 从重构的模块导入所有公开的类和函数
from .camera import Camera
from .processor import Processor, ProcessedCamera, apply_effect

def cv_show(frame, mode="cv2", wait_key=1):
    """
    显示图像并处理按键
    
    此函数为兼容性提供，建议直接使用Camera.cv_show方法
    
    参数:
        frame: 要显示的图像帧
        mode: 显示模式，"cv2"表示本地显示，"web"表示网页显示
        wait_key: cv2.waitKey的等待时间，单位为毫秒（仅在cv2模式下有效）
    
    返回:
        如果按下'q'则返回True，否则返回False
        
    注意:
        此函数仅提供本地显示模式。如果您想使用"web"模式，
        请使用Camera实例的cv_show方法：
        cam.cv_show(frame, "web")
        
    示例:
    ```python
    from aitoolkit_cam import Camera, cv_show
    
    cam = Camera(0)
    url = cam.start()
    print(f"请在局域网内通过浏览器访问: {url}")
    
    for frame in cam:
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 在网页上显示灰度图（使用Camera实例的方法）
        cam.cv_show(gray, "web")
        
        # 在本地窗口显示灰度图
        if cv_show(gray, "cv2"):  # 或使用 cam.cv_show(gray, "cv2")
            break  # 按下q退出循环
            
    cam.stop()
    ```
    """
    import cv2
    
    if frame is None:
        return False
    
    # 只支持本地显示模式
    if mode.lower() == "web":
        print("警告：全局cv_show函数不支持web模式，请使用Camera实例的cv_show方法")
        return False
    
    # 本地显示模式
    display_frame = frame
    if len(frame.shape) == 2:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        
    # 显示图像
    cv2.imshow("预览", display_frame)
    
    # 等待按键并检查是否按下q键
    key = cv2.waitKey(wait_key) & 0xFF
    return key == ord('q')

# 指定公开的API
__all__ = ['Camera', 'Processor', 'ProcessedCamera', 'apply_effect', 'cv_show']

# 版本信息
__version__ = '0.2.0' 