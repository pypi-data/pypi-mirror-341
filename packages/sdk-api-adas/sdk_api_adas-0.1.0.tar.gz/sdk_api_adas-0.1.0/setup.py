from setuptools import setup, find_packages

setup(
    name="sdk-api-adas",  # Nombre del paquete
    version="0.1.0",  # Versión inicial
    description="SDK para interactuar con la API ADAS protegida por AWS IAM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tu Nombre",
    author_email="jose.salamanca@softgic.co",
    url="https://github.com/Transportes-Rapido-Ochoa/sdk-api-adas",  # URL del repositorio
    packages=find_packages(exclude=["examples", "tests","scripts"]),
    install_requires=[
        "pydantic>=1.10.0",  # Dependencias necesarias
        "boto3>=1.20.0",
        "requests>=2.32.3",
        "requests_aws4auth"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
