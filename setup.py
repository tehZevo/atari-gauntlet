from setuptools import setup, find_packages

setup(name='atari-gauntlet',
  version='0.0.0',
  install_requires = [
    "retro",
    "numpy",
    "gym"
  ],
  packages=find_packages())
