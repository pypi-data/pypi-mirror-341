
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-google-sheets",
    version="0.2.0",
    description="This MCP server integrates with your Google Drive and Google Sheets, to enable creating and modifying spreadsheets.",
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
    install_requires=['mcp>=1.5.0', 'google-auth>=2.28.1', 'google-auth-oauthlib>=1.2.0', 'google-api-python-client>=2.117.0'],
    keywords=["mseep"] + [],
)
