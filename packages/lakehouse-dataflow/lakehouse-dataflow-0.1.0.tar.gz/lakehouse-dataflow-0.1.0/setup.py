from setuptools import setup, find_packages

setup(
    name="lakehouse-dataflow",
    version="0.1.0",
    description="Pipeline de dados da Lakehouse",
    author="superfrete",
    author_email="guilherme.caly@superfrete.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.0.0",
    ],
    python_requires=">=3.8",
)
