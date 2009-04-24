from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='helloworld',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "webob",
          "PasteDeploy",
          "PasteScript",
      ],
      entry_points={
          "paste.app_factory": [ 
              "printenv=helloworld.printenv:factory",
              ],
          "paste.filter_app_factory": [
              "file_server=helloworld.fileserver:FileServer",
              ],
      },
      )
