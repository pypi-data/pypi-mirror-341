from setuptools import setup, find_packages

setup(
    name="pacote-TratImagem-Junior-de-freitas",  # Nome único (teste)
    version="0.1.0",
    author="Junior de |Freitas",
    author_email="juniordefreitas1@gmail.com",
    description="Funções para manipulação e visualização de imagens com scikit-image.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["numpy", "matplotlib", "scikit-image"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
