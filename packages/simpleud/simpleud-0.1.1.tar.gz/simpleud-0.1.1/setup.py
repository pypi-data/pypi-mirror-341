from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simpleud",
    version="0.1.1",
    author="Sugar Knight",
    author_email="your.email@example.com",
    description="シンプルなファイルアップロード・ダウンロードライブラリ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sugarkwork/simpleud",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.7.0",
        "urllib3>=1.26.0",
    ],
)