
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-headless-gmail",
    version="0.1.0",
    description="A simple Gmail MCP server",
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
    install_requires=['mcp>=1.4.1', 'python-dotenv>=1.0.1', 'google-api-python-client>=2.127.0', 'google-auth>=2.34.0', 'google-auth-oauthlib>=1.2.0', 'google-auth-httplib2>=0.2.0', 'python-dateutil>=2.8.2'],
    keywords=["mseep"] + [],
)
