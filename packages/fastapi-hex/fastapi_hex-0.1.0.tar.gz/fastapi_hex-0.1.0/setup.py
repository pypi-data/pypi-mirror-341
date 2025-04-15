from setuptools import setup, find_packages

setup(
    name="fastapi_hex",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fastapi-hex=fastapi_hex.cli:main",
        ],
    },
    install_requires=["fastapi"],
    description="Generador de proyectos FastAPI con arquitectura Hexagonal.",
    author="Juan",
    author_email="tuemail@example.com",
)
