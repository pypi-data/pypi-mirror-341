from setuptools import setup, find_packages

setup(
    name="fei_cpp_library",  # 你的包名
    version="0.1.3",    # 版本号
    packages=find_packages(),  # 自动发现所有包
    install_requires=[  # 列出依赖的库
        "requests",  # 举例依赖，实际可以是你需要的库
        "boto3"
    ],
    long_description=open('README.md').read(),  # 包的说明，通常从 README.md 中读取
    long_description_content_type='text/markdown',  # 说明文件类型
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 支持的 Python 版本
)
