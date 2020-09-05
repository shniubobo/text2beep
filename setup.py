"""\
This file is part of text2beep.

Copyright (C) 2020 shniubobo

text2beep is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

text2beep is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
text2beep. If not, see <https://www.gnu.org/licenses/>.
"""
from setuptools import find_packages, setup

from text2beep.version import get_version

with open('README_en.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='text2beep',
    version=get_version(),
    description='A CLI tool that converts plaintext sheet music to beeps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='shniubobo',
    author_email='shniubobo@outlook.com',
    url='https://github.com/shniubobo/text2beep',
    project_urls={
        'Source': 'https://github.com/shniubobo/text2beep',
        'Issue Tracker': 'https://github.com/shniubobo/text2beep/issues',
    },
    license='GPL-3.0-or-later',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(),
    include_pacakge_data=True,
    python_requires='>=3.6, <4',
    install_requires=[
        'numpy~=1.19.1',
        'sounddevice~=0.4.0',
    ],
    extras_require={
        'dev': [
            'coverage[toml]~=5.2.1',
            'flake8~=3.8.3',
            'pytest>=6.0',
            'pytest-cov~=2.10.1',
            'pytest-timeout~=1.4.2',
        ],
    },
    entry_points={
        'console_scripts': [
            'text2beep = text2beep.__main__:main',
        ],
    },
)
