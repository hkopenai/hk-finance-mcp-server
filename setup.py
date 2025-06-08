import os
from setuptools import setup, find_packages

setup(
    name="hk-finance-mcp-server",
    version="0.1.1",
    description="Hong Kong Finance MCP Server providing financial data tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=(
        open("requirements.txt").read().splitlines()
        if os.path.exists("requirements.txt")
        else []
    ),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'hk-finance-mcp-server=hk_finance_mcp_server.app:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
