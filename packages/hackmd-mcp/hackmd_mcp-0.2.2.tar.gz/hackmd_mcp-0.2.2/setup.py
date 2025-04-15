from setuptools import setup, find_packages
from hackmd_mcp import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hackmd-mcp",
    version=__version__,
    author="Oliver",
    author_email="your.email@example.com",
    description="A command line utility for HackMD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hackmd_mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "hackmd-mcp=hackmd_mcp.cli:main",
        ],
    },
    install_requires=[
        # 添加您的依賴庫
        # 例如 "requests>=2.25.1",
    ],
)
