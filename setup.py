#!/usr/bin/env python
#
# Copyright 2009 comger@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

kwargs = {}


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires



setup(name="fastapicli",
      version="0.0.2",
      packages=find_packages(where='.', exclude=(), include=('*',)),
      package_data={'': ['*.*']},
      exclude_package_data={'': ["*.pyc"]},
      author="comger@gmail.com",
      author_email="comger@gmail.com",
      url="http://github.com/comger/fastapicli",
      license="http://www.apache.org/licenses/LICENSE-2.0",
      description="fastapicli is a easy tool for fastapi orm with jwt",
      scripts=['fastapicli/fastapi_init.py','fastapicli/fastapi_api.py'],
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      keywords=["fastapi", "orm", "peewee", "jwt", "codegen"],
      install_requires=["tornado"],
      **kwargs)
