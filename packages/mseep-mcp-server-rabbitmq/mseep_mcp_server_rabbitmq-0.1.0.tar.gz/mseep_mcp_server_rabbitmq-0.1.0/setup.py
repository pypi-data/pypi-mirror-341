
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-rabbitmq",
    version="0.1.0",
    description="A Model Context Protocol server providing access to RabbitMQ by LLMs",
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
    install_requires=['markdownify>=0.13.1', 'mcp>=1.1.2', 'pika>=1.3.2', 'protego>=0.3.1', 'pydantic>=2.0.0', 'readabilipy>=0.2.0', 'requests>=2.32.3'],
    keywords=["mseep"] + ['rabbitmq', 'mcp', 'llm', 'automation'],
)
