# AIToolkit Camera

一个简单易用的摄像头工具包，支持本地显示和网页显示。

## 功能特性

- 支持摄像头图像的本地显示和网页显示
- 支持多种图像处理效果（灰度、边缘检测、模糊、素描、卡通）
- 支持使用`for`循环迭代获取摄像头帧
- 简单易用的API接口

## 安装方法

```bash
pip install aitoolkit-cam
```

## 使用示例

```python
from aitoolkit_cam import Camera, ProcessedCamera, cv_show

# 基本用法
cam = Camera(0)  # 使用索引为0的摄像头
for frame in cam:
    if cv_show(frame, "web"):  # 在网页中显示
        break

# 本地显示
cam = Camera(0)
for frame in cam:
    if cv_show(frame, "cv2"):  # 本地窗口显示
        break

# 使用图像处理效果
proc_cam = ProcessedCamera(0, effect_type="sketch")
for frame in proc_cam:
    if cv_show(frame, "web"):
        break
```

## 网页显示

使用网页显示模式时，打开浏览器访问：http://localhost:8000

## 许可证

MIT 