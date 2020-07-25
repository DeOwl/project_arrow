from setuptools import setup, find_packages

setup(
    name='Tello modules',
    version='0.2',
    packages=find_packages(),
    install_requires=['pyserial'],
	long_description=open('README.md').read()
)
