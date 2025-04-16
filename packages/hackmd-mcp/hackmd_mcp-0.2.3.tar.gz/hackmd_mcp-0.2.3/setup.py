from setuptools import setup, find_packages
import os

# 讀取版本號
with open(os.path.join("hackmd_mcp", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

# 讀取 README 內容
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "HackMD MCP - 命令行工具與 MCP 服務"

setup(
    name="hackmd-mcp",
    version=version,
    author="Oliver",
    author_email="your.email@example.com",
    description="HackMD MCP - 命令行工具與 MCP 服務",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hackmd-mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "httpx>=0.20.0",
        "pydantic>=2.0.0",
        "mcp>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "hackmd-mcp=hackmd_mcp.hackmd_mcp_server:main",
        ],
    },
)
