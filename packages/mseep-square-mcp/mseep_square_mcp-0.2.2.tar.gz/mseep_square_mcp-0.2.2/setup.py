
from setuptools import setup, find_packages

setup(
    name="mseep-square-mcp",
    version="0.2.2",
    description="Square API Model Context Protocol Server",
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
    install_requires=['mcp[cli]>=1.2.0', 'squareup>=33.1.0'],
    keywords=["mseep"] + ['square', 'mcp', 'api', 'payments'],
)
