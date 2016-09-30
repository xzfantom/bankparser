#!/usr/bin/python3
"""Setup
"""
import distutils.cmd
import distutils.command.build as _build
from setuptools import find_packages
from distutils.core import setup
from distutils.command.install import install as _install
from distutils.command.build_py import build_py
#from distutils import command as _build_py
#from distutils.cmd import Command
#from distutils.cmd import Command as command
import build
version = "0.0.1"

# Генерация файлов и справки
#mybuild = build.MyBuild()
#mybuild.gen_files()

class mybuild(build_py):
    def run(self):
        print('Here MyBuild')
        #distutils.command.build.run(self)
        build_py.run(self)



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
      description=("Sample plugin for ofxstatement"),
      long_description=long_description,
      license="GPLv3",
      keywords=["qif", "banking", "statement"],

      cmdclass={'copyscript':copyscript, 'genfiles': genfiles},

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

      package_dir={'bankparser': 'src'},


      package_data={'bankparser': ['*.ini']},

      # install_requires=['setuptools',
      #                   'appdirs'
      #                   ],
      #namespace_packages=["bankparser"],

      entry_points={
          'console_scripts':
          ['bankparser = bankparser.bankparsercli:main'],
      },
      #include_package_data=True,
      #zip_safe=True
      )


