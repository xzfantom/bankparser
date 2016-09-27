#!/usr/bin/python3
"""Setup
"""
from setuptools import find_packages
from distutils.core import setup
import build
version = "0.0.1"

# Генерация файлов и справки
mybuild = build.MyBuild()
mybuild.gen_files()

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
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: Russian',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["bankparser"],
      #scripts=['src/bankparser/bankparsercli.py'],
      entry_points={
          'console_scripts':
          ['bankparser = bankparser.bankparsercli:main'],
      },
      include_package_data=True,
      zip_safe=True
      )


