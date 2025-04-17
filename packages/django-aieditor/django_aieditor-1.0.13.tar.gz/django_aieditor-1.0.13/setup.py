from setuptools import setup, find_packages
import io

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="django-aieditor",
    version="1.0.13",
    packages=find_packages(),
    include_package_data=True,
)