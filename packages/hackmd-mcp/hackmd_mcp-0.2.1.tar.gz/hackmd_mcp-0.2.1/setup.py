from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hackmd_mcp",
    version="0.2.1",
    author="Oliver0804",
    author_email="icetzsr@gmail.com",
    description="A package for HackMD functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Oliver0804/hackmd_mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        # 在這裡添加你的依賴項
        "httpx",
        "mcp",
        "pydantic"
    ],
    entry_points={
        'console_scripts': [
            'hackmd-mcp=hackmd_mcp_server:main',  # 修改這行，移除 hackmd_mcp. 前綴
        ],
    },
)
