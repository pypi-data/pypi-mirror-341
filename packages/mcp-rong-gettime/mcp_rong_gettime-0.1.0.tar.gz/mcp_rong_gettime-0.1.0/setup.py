from setuptools import setup, find_packages

setup(
    name="mcp_rong_gettime",  # 包名，pip install 时用这个
    version="0.1.0",
    description="A simple hello tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="rong",
    author_email="35050456257@qq.com",
    url="https://github.com/你的用户名/mytool",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)