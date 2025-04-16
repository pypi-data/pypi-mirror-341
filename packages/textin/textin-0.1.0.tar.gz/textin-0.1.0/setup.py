from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-textin",
    version="0.1.0",
    author="Ke Wang",
    description="TextIn API Service for MCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/modelcontextprotocol/mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "mcp-sdk>=0.1.0"
    ],
    entry_points={
        "mcp.services": [
            "textin=textin.server:mcp"
        ]
    }
)