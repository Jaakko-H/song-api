from setuptools import find_packages, setup

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

setup(
    name='Song API',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements
)
