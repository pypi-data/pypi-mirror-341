from setuptools import setup, find_packages

setup(
    name="yala-events-mcp",
    version="0.1.0",
    author="Yala Events",
    author_email="your.email@example.com",  # Update with your email
    description="MCP server for Yala Events with stdio transport",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yala-events-mcp",  # Update with your repo URL
    packages=find_packages(),
    install_requires=[
        "httpx",
        "python-dotenv",
        "mcp-sdk>=0.1.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "yala-events-mcp=yala_events_mcp.server:main",
        ],
    },
)
