
from setuptools import setup, find_packages

setup(
    name="mseep-age-mcp-server",
    version="0.2.9",
    description="Apache AGE MCP Server",
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
    install_requires=['agefreighter>=1.0.4', 'mcp>=1.5.0', 'ply>=3.11', 'psycopg[binary,pool]>=3.2.6'],
    keywords=["mseep"] + [],
)
