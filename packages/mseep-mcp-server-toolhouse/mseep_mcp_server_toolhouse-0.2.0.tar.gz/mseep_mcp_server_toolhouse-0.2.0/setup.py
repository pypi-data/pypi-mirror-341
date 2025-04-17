
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-toolhouse",
    version="0.2.0",
    description="All the high-quality toolhouse tools in one place, accessible as one MCP server",
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
    install_requires=['mcp>=1.2', 'httpx>=0.28.1'],
    keywords=["mseep"] + [],
)
