from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aitoolkit-cam",
    version="0.1.1",
    author="AIToolkit",
    author_email="your.email@example.com",
    description="简单易用的摄像头工具包，支持本地显示和网页显示",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aitoolkit-cam",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "opencv-python>=4.5.0",
        "vidgear>=0.2.5",
        "uvicorn>=0.17.0",
        "starlette>=0.17.1",
        "numpy>=1.19.0",
    ],
    keywords="camera, video, webcam, computer vision, opencv",
) 