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
import logging
from pathlib import Path

from text2beep.__main__ import main
from text2beep.version import get_version


class DummyOutputStream:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def write(audio):
        print(f'Writing to stream: {audio}')


def test_main(monkeypatch, capsys, caplog):
    with monkeypatch.context() as m:
        m.setattr('sys.argv', ['text2beep'])
        try:
            main()
        except SystemExit:
            pass
        stdout, stderr = capsys.readouterr()
        assert 'error: the following arguments are required:' in stderr

    with monkeypatch.context() as m:
        m.setattr('sys.argv', ['text2beep', '-h'])
        try:
            main()
        except SystemExit:
            pass
        stdout, stderr = capsys.readouterr()
        assert 'positional arguments:\n' in stdout

    with monkeypatch.context() as m:
        m.setattr('sys.argv', ['text2beep', '-v', 'file'])
        logging.basicConfig(level=logging.INFO)
        try:
            main()
        except FileNotFoundError:
            pass
        assert logging.root.level == logging.DEBUG

    with monkeypatch.context() as m:
        m.setattr('sys.argv', ['text2beep', '-V'])
        try:
            main()
        except SystemExit:
            pass
        stdout, stderr = capsys.readouterr()
        assert stdout == f'text2beep {get_version()}\n'

    with monkeypatch.context() as m:
        m.setattr('sys.argv',
                  ['text2beep', str(Path('examples/Am-F-G-C.json'))])
        m.setattr('sounddevice.OutputStream', DummyOutputStream)
        main()
        assert 'Playing ' in caplog.text
        stdout, _ = capsys.readouterr()
        assert stdout.count('Writing to stream: ') == 4

        m.setattr('sys.argv',
                  ['text2beep', '-q', str(Path('examples/Am-F-G-C.json'))])
        main()
