
from setuptools import setup, find_packages

setup(
    name="mseep-mac-messages-mcp",
    version="0.6.5",
    description="A bridge for interacting with macOS Messages app through MCP",
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
    install_requires=['mcp[cli]'],
    keywords=["mseep"] + ['macos', 'messages', 'imessage', 'mcp'],
)
