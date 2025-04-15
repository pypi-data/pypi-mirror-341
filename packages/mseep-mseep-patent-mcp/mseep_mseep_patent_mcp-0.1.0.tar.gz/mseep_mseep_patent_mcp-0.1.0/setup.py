from setuptools import setup, find_packages

setup(
    name="mseep-patent_mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'aiohttp>=3.8.1',
        'python-dotenv>=0.19.0',
    ],
    python_requires='>=3.11',
)