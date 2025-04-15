
from setuptools import setup, find_packages

setup(
    name="orange1-modal-server",
    version="0.1.0",
    description="",
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
    install_requires=['httpx>=0.28.1', 'mcp>=1.1.1', 'python-dotenv>=1.0.1', 'modal>=0.67'],
    keywords=["orange1"] + [],
)
