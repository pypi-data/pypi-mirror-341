from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cmdinput",
    version="1.0.0",
    author="klarkxy",  # 需要替换为实际作者名
    author_email="278370456@qq.com",  # 需要替换为实际邮箱
    description="A flexible command-line input parsing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/klarkxy/cmdinput",  # 需要替换为实际项目URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],  # 没有第三方依赖
    extras_require={
        "dev": ["twine>=4.0.2"],
        "test": ["pytest>=7.0.0"],
    },
    entry_points={
        "console_scripts": [
            # 如果没有命令行工具可留空
        ],
    },
)

# 使用说明：
# 1. 填写作者信息、邮箱和项目URL
# 2. 创建源码包和wheel: python setup.py sdist bdist_wheel
# 3. 上传到PyPI: twine upload dist/*
