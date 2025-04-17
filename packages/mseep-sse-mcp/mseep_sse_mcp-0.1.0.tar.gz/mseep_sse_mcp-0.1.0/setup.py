
from setuptools import setup, find_packages

setup(
    name="mseep-sse-mcp",
    version="0.1.0",
    description="Add your description here",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp>=1.0.0', 'mysql-connector-python>=9.2.0', 'pypinyin>=0.54.0', 'python-dotenv>=1.1.0', 'starlette>=0.46.1', 'uvicorn>=0.34.0'],
    keywords=["mseep"] + [],
)
