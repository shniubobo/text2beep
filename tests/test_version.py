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
import re
import subprocess as sp

from text2beep.version import *


def test_constants():
    assert isinstance(MAJOR, int)
    assert isinstance(MINOR, int)
    assert isinstance(PATCH, int)
    assert POST is None or isinstance(POST, int)


def test_get_version(tmp_path, monkeypatch):
    with monkeypatch.context() as m:
        m.chdir(tmp_path)
        sp.run(['git', 'init'])

        with open('some_file.txt', 'w') as f:
            f.write('some text\n')
        assert get_version() == f'{MAJOR}.{MINOR}.{PATCH}+dirty'

        sp.run(['git', 'add', 'some_file.txt'])
        sp.run(['git', 'commit', '-m', 'commit 1'])
        public_version = f'{MAJOR}\\.{MINOR}\\.{PATCH}'
        assert re.match(public_version + r'\+1\.[0-9a-f]{7}',
                        get_version())

        with open('some_file.txt', 'a') as f:
            f.write('more text\n')
        assert re.match(public_version + r'\+1\.[0-9a-f]{7}\.dirty',
                        get_version())

        sp.run(['git', 'add', 'some_file.txt'])
        sp.run(['git', 'commit', '-m', 'commit 2'])
        assert re.match(public_version + r'\+2\.[0-9a-f]{7}',
                        get_version())

        sp.run(['git', 'tag', 'v0.1.0'])
        assert get_version() == f'{MAJOR}.{MINOR}.{PATCH}'

        m.setattr('text2beep.version.POST', 1)
        assert get_version() == f'{MAJOR}.{MINOR}.{PATCH}.post1'

        with open('some_file.txt', 'a') as f:
            f.write('more text\n')
        sp.run(['git', 'add', 'some_file.txt'])
        sp.run(['git', 'commit', '-m', 'commit 3'])
        assert re.match(public_version + r'\.post1\+1\.[0-9a-f]{7}',
                        get_version())
