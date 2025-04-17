
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-atlassian",
    version="0.7.0",
    description="The Model Context Protocol (MCP) Atlassian integration is an open-source implementation that bridges Atlassian products (Jira and Confluence) with AI language models following Anthropic's MCP specification. This project enables secure, contextual AI interactions with Atlassian tools while maintaining data privacy and security. Key features include:",
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
    install_requires=['atlassian-python-api>=3.41.16', 'beautifulsoup4>=4.12.3', 'httpx>=0.28.0', 'mcp>=1.3.0', 'python-dotenv>=1.0.1', 'markdownify>=0.11.6', 'markdown>=3.7.0', 'markdown-to-confluence>=0.3.0', 'pydantic>=2.10.6', 'trio>=0.29.0', 'click>=8.1.7', 'uvicorn>=0.27.1', 'starlette>=0.37.1'],
    keywords=["mseep"] + [],
)
