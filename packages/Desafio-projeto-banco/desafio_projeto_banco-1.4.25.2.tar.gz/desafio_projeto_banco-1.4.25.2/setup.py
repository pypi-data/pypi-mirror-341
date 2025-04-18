from setuptools import setup, find_packages


setup(
    name="Desafio_projeto_banco",
    version="1.04.25.2",
    author="Igor Mekaro",
    author_email="iguinhoo.msn@hotmail.com",
    description="É um projeto de banco, um desafio proposto pela DIO.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/mekaroi/Desafio_projeto_banco",
    python_requires=">=3.6",
    license="MIT,"
)
