from setuptools import setup, find_packages

setup(
    name='Tello modules',
    version='0.1dev',
    packages=find_packages(),
    install_requires=['pyserial']
)
