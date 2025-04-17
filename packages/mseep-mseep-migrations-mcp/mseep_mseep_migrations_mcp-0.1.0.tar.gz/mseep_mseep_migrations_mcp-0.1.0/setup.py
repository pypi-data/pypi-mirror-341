from setuptools import setup, find_packages

setup(
    name="mseep-migrations-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=5.1.0",
        "mcp",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "structlog>=23.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.4.1",
            "pylint>=2.17.5",
        ]
    },
) 