from setuptools import setup, find_packages

setup(
    name="finite_time_optim",  # 你的包的名字
    version="0.1.0",  # 版本号
    packages=find_packages(),  # 自动发现所有的包（包括 `finite_time_optim`）
    install_requires=[ 
        "torch",     ],
    author="Yu Zhou",  # 作者名字
    author_email="yu_zhou@yeah.net",
    description="A collection of finite-time optimization algorithms.",  
    # long_description=open('README.md').read(),  # 读取 README 文件作为详细描述
    long_description_content_type="text/markdown",  # README 文件格式
    url="https://github.com/your_username/finite_time_optim",  # GitHub 项目链接
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 你的包支持的Python版本
)
