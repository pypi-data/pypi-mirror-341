
from setuptools import setup, find_packages

setup(
    name="mseep-aipolabs-mcp",
    version="0.0.1b5",
    description="Aipolabs MCP server, built on top of ACI.dev",
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
    install_requires=['aipolabs>=0.0.1b7', 'anthropic>=0.49.0', 'anyio>=4.9.0', 'click>=8.1.8', 'mcp>=1.4.1', 'starlette>=0.46.1', 'uvicorn>=0.34.0'],
    keywords=["mseep"] + ['aipolabs', 'mcp', 'aci', 'mcp server', 'llm', 'tool calling', 'function calling'],
)
