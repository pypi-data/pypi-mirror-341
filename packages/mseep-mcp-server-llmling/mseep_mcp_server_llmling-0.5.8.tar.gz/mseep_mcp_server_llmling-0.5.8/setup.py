
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-llmling",
    version="None",
    description="MCP (Model context protocol) server with LLMling backend",
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
    install_requires=['fastapi[standard]>=0.115.6', 'universal-pathlib>=0.2.5', 'uvicorn', 'llmling>=1.0.0', 'mcp>=1.1.0', 'pydantic', 'logfire>=2.6.2', 'websockets>=14.1', 'upathtools[httpx]'],
    keywords=["mseep"] + [],
)
