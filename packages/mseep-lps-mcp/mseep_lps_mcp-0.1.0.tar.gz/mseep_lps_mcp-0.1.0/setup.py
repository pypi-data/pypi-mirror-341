
from setuptools import setup, find_packages

setup(
    name="mseep-lps-mcp",
    version="0.1.0",
    description="Un servidor MCP mínimo para permitir a Claude interactuar con archivos locales. Solo lectura. Incluido con pensamiento extendido.",
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
    install_requires=['mcp[cli]>=1.4.1'],
    keywords=["mseep"] + [],
)
