from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cursor-gitlab-mcp",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9.0",
        "python-gitlab>=3.15.0",
        "urllib3>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cursor-gitlab-mcp=gitlab_mcp.server:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="GitLab MCP service for Cursor IDE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cursor-gitlab-mcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 