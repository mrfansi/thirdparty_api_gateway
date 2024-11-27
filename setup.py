from setuptools import setup, find_packages

setup(
    name="thirdparty_api_gateway",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests",
        "pydantic",
        "pytest",
        "pytest-asyncio",
        "pytest-mock"
    ],
)
