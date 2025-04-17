#from distutils.core import setup # type: ignore
from setuptools import setup#, find_packages

setup(name='pnh',
      version='0.0.4',
      description='pnh',
      packages=['pnh','pnh.utils'],#find_packages(),
      package_dir={
      'pnh':'.','pnh.utils':'utils'},
     )