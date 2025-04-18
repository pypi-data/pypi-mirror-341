from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name='BacenAPI',
    version='0.1.0',
    license='MIT',
    author='Paulo Icaro, Lissandro Sousa, Francisco Gildemir',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lisandrosousa54@gmail.com',
    keywords='time-serie, api_data, central_bank',
    description='tools for manipulating time series data from the Central Bank of Brazil',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    include_package_data=True,
    package_data={
        "BacenAPI": ["Date/*.txt", "Date/*.parquet"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',)