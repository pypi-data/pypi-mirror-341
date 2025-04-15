from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hackmd_mcp",
    version="0.1.0",
    author="Your Name",
    author_email="icetzsr@gmail.com",
    description="A package for HackMD functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hackmd_mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        # 在這裡添加你的依賴項
    ],
)
