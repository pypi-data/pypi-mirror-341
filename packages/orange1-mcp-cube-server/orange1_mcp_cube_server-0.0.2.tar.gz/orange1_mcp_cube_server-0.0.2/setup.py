
from setuptools import setup, find_packages

setup(
    name="orange1-mcp_cube_server",
    version="0.0.2",
    description="MCP server for interfacing with Cube.dev REST API",
    author="orange1",
    author_email="support@orange.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp>=1.2.1', 'pandas', 'pyjwt>=2.10.1', 'python-dotenv', 'pyyaml>=6.0.2', 'requests>=2.32.3'],
    keywords=["orange1"] + [],
)
