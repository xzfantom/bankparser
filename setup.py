#!/usr/bin/python3
"""Setup
"""
import distutils.cmd
#from distutils.core import setup
from setuptools import find_packages
from setuptools import setup
#from distutils.cmd setuptools.command.test import test as TestCommand
from setuptools.command.test import test as TestCommand
#import setuptools.command
import unittest
import sys

import build
version = "0.0.1"


class RunTests(TestCommand):
    """New setup.py command to run all tests for the package.
    """
    description = "run all tests for the package"

    def finalize_options(self):
        super(RunTests, self).finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        tests = unittest.TestLoader().discover('src/bankparser')
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(tests)
        sys.exit(not res.wasSuccessful())


class genfiles(distutils.cmd.Command):
    user_options = []
    description = 'generate .py and readme command'
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        mybuild = build.MyBuild()
        mybuild.buid()

class copyscript(distutils.cmd.Command):
    #user_options = []
    user_options = [('pubdir=', None, 'Specify dir for public')]
    description = 'copy script for testing command'
    def initialize_options(self):
        self.pubdir = None

    def finalize_options(self):
        pass

    def run(self):
        #self.run()
        #print('MyBuild')
        mybuild = build.MyBuild(self.pubdir)
        mybuild.copy_script()
        #_build_py.run(self)


with open('README.rst',encoding='utf-8') as f:
    long_description = f.read()



setup(name='bankparser',
      version=version,
      author="Andrey Kapustin",
      author_email="",
      url="https://github.com/partizand/bankparser",
      description=("Convert banks statements to qif fiormat"),
      long_description=long_description,
      license="GPLv3",
      keywords=["qif", "banking", "statement"],

      cmdclass={'test': RunTests, 'copyscript':copyscript, 'genfiles': genfiles},

      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: Russian',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3'],

      #packages=find_packages('src'),



      packages=['bankparser'],

      package_dir={'': 'src'},


      #package_data={'bankparser': ['*.ini']},

      install_requires=['setuptools'],
      #                   'appdirs'
      #                   ],
      #namespace_packages=["bankparser"],

      entry_points={
          'console_scripts':
          ['bankparser = bankparser.bankparsercli:main'],
      },
      include_package_data=True,
      zip_safe=False
      )


