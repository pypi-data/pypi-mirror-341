
from setuptools import setup, find_packages

setup(
    name="orange1-pagerduty_mcp_server",
    version="v2.2.0",
    description="MCP server for LLM agents to interact with PagerDuty SaaS",
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
    install_requires=['mcp>=1.3.0', 'pagerduty>=1.0.0', 'pytest>=8.3.5', 'ruff>=0.11.2'],
    keywords=["orange1"] + ['pagerduty', 'mcp', 'llm', 'api', 'server'],
)
