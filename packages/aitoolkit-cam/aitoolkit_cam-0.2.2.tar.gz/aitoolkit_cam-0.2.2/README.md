# AIToolkit Camera - 简易摄像头工具包

![版本](https://img.shields.io/badge/版本-0.2.2-blue)
![Python 版本](https://img.shields.io/badge/Python-3.7+-brightgreen)
![许可证](https://img.shields.io/badge/许可证-MIT-green)

`aitoolkit_cam` 是一个针对Python的简单易用的摄像头工具包，让摄像头开发变得轻松简单。无论您是教育工作者还是学生，都可以通过几行代码轻松实现摄像头功能。

## 核心特点

- 🌟 **简单易用**：几行代码即可启动摄像头和网页服务
- 🌐 **网页实时查看**：支持通过浏览器远程查看摄像头画面
- 🔄 **迭代器接口**：兼容Python迭代器，可在for循环中使用
- 🖼️ **图像处理**：支持基础图像处理功能
- 🔌 **资源管理**：自动释放摄像头资源

## 安装方法

```bash
pip install aitoolkit-cam
```

## 基础用法

### 简单示例

```python
from aitoolkit_cam import Camera

# 创建摄像头对象
cam = Camera()
cam.web_enabled = True  # 启用网页服务

# 启动摄像头
cam.start()

# 获取访问地址
url = cam.get_web_url()
print(f"访问地址: {url}")
print("请在浏览器中访问上述地址")

try:
    # 循环获取视频帧并在网页显示
    for frame in cam:
        cam.cv_show(frame, "web")
except KeyboardInterrupt:
    print("正在退出...")
finally:
    # 释放资源
    cam.stop()
```

### Jupyter Notebook中使用

```python
from aitoolkit_cam import Camera
import threading
import time

# 全局变量
cam = None
running = True

def stop_camera():
    """停止摄像头"""
    global cam, running
    running = False
    if cam:
        print("正在停止摄像头...")
        cam.stop()
        time.sleep(0.5)
        print("摄像头已停止")
    return "摄像头已停止，资源已释放"

def camera_loop(camera):
    """摄像头循环"""
    global running
    try:
        for frame in camera:
            if not running:
                break
            camera.cv_show(frame, "web")
    except Exception as e:
        print(f"摄像头循环错误: {e}")
    finally:
        if running:
            running = False
            camera.stop()

def start_camera():
    """启动摄像头"""
    global cam, running
    
    # 如果已有运行实例，先停止
    if cam and running:
        stop_camera()
    
    running = True
    
    # 创建摄像头对象
    cam = Camera()
    cam.web_enabled = True
    
    # 启动摄像头
    print("正在启动摄像头和网页服务...")
    start_time = time.time()
    cam.start()
    
    # 获取地址
    url = cam.get_web_url()
    print(f"启动耗时: {time.time() - start_time:.2f}秒")
    print(f"访问地址: {url}")
    
    # 在后台线程中运行摄像头循环
    thread = threading.Thread(target=camera_loop, args=(cam,), daemon=True)
    thread.start()
    
    print("摄像头已在后台运行")
    print("使用 stop_camera() 函数停止摄像头")
    return url

# 使用方法：
# 1. 运行 start_camera() 启动摄像头
# 2. 使用返回的URL访问摄像头画面
# 3. 完成后运行 stop_camera() 释放资源
```

## 高级用法

### 使用反向代理解决端口变化问题

当需要在前端页面或其他应用中嵌入摄像头画面时，可以使用反向代理保持URL稳定：

#### 1. 安装Nginx

```bash
# 在Ubuntu/Debian上
sudo apt install nginx

# 在CentOS/RHEL上
sudo yum install nginx

# 在Windows上可以下载安装包
# http://nginx.org/en/download.html
```

#### 2. 配置Nginx反向代理

创建或编辑Nginx配置文件（例如`/etc/nginx/conf.d/camera.conf`）：

```nginx
server {
    listen 80;
    server_name your_server_name;  # 修改为您的服务器名称或IP

    location /camera/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_read_timeout 86400;
    }
}
```

#### 3. 启动摄像头服务和Nginx

```bash
# 重启Nginx应用配置
sudo systemctl restart nginx

# 启动摄像头服务（端口固定为8000）
python -c "
from aitoolkit_cam import Camera
cam = Camera()
cam.web_enabled = True
cam.port = 8000
cam.start()
print(f'摄像头服务已启动: {cam.get_web_url()}')
input('按Enter键退出...')
cam.stop()
"
```

现在可以通过 `http://your_server_name/camera/` 访问摄像头，无论底层摄像头服务端口如何变化。

### 在前端页面中嵌入摄像头画面

使用反向代理后，可以在HTML页面中嵌入摄像头画面：

```html
<!DOCTYPE html>
<html>
<head>
    <title>摄像头画面</title>
    <style>
        .camera-container {
            width: 640px;
            height: 480px;
            margin: 0 auto;
            border: 1px solid #ccc;
            overflow: hidden;
        }
        .camera-feed {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
    </style>
</head>
<body>
    <div class="camera-container">
        <img src="http://your_server_name/camera/video" class="camera-feed" alt="摄像头画面">
    </div>
</body>
</html>
```

## 进阶功能

### 图像处理

```python
from aitoolkit_cam import Camera, apply_effect

# 创建摄像头对象
cam = Camera()
cam.web_enabled = True
cam.start()

# 应用图像效果
for frame in cam:
    # 应用灰度效果
    processed = apply_effect(frame, "grayscale")
    cam.cv_show(processed, "web")
```

### 使用上下文管理器

```python
from aitoolkit_cam import Camera

# 使用with语句自动管理资源
with Camera() as cam:
    cam.web_enabled = True
    cam.start()
    url = cam.get_web_url()
    print(f"访问地址: {url}")
    
    # 处理10帧后退出
    count = 0
    for frame in cam:
        cam.cv_show(frame, "web")
        count += 1
        if count >= 10:
            break

# with语句结束后自动释放资源
```

## 开发者信息

- 作者：[您的名字]
- 版本：0.2.2
- 许可证：MIT

## 贡献

欢迎提交问题和贡献代码以改进这个项目！ 