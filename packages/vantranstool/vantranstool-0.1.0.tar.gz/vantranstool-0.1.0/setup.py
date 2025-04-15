from setuptools import setup, find_packages

setup(
    name="vantransTool",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp-client>=0.1.0",
        "mcp-server>=0.1.0",
        "requests>=2.31.0",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
    ],
    python_requires=">=3.8",
    author="baiyx",
    author_email="baiyx@example.com",
    description="一个基于MCP协议的运输工具服务，提供批量外部派车功能",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vantransTool",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 