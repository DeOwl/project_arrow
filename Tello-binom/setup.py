from setuptools import setup,find_packages
setup(
      name = 'Tello',
      version = '2.1',
      py_modules=['tello_binom'],
      install_requires = [
          'opencv-python',
          'pillow',
          'pygame'
      ]
  )
