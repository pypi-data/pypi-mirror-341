
from setuptools import setup, find_packages

setup(
    name="mseep-singlestore_mcp_server",
    version="None",
    description="SingleStore MCP server",
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
    install_requires=['mcp>=1.3.0', 's2-ai-tools>=1.0.6', 'singlestoredb>=1.12.0'],
    keywords=["mseep"] + [],
)
