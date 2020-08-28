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
import subprocess as sp

__all__ = [
    'MAJOR',
    'MINOR',
    'PATCH',
    'POST',
    'get_version',
]

MAJOR = 0
MINOR = 0
PATCH = 0
POST = None


def get_version():
    version = [f'{MAJOR}.{MINOR}.{PATCH}']
    if POST is not None:
        version.append(f'.post{POST}')
    try:
        commits_since_last_tag, last_commit_hash = _get_local_changes()
    except TypeError:
        if _is_dirty():
            version.append('+dirty')
    else:
        version.append(f'+{commits_since_last_tag}.{last_commit_hash}')
        if _is_dirty():
            version.append('.dirty')
    return ''.join(version)


def _get_local_changes():
    proc = sp.run(
        ['git', 'rev-list', '--tags', '--max-count=1', '--abbrev-commit'],
        capture_output=True)
    last_tag_hash = proc.stdout.decode().strip('\n')
    proc = sp.run(['git', 'log', '-1', '--format=%h'], capture_output=True)
    last_commit_hash = proc.stdout.decode().strip('\n')
    if last_tag_hash == last_commit_hash:
        return None
    if last_tag_hash:
        commit_range = f'{last_tag_hash}..HEAD'
    else:
        commit_range = 'HEAD'
    proc = sp.run(['git', 'rev-list', commit_range, '--count'],
                  capture_output=True)
    commits_since_last_tag = proc.stdout.decode().strip('\n')
    return commits_since_last_tag, last_commit_hash


def _is_dirty():
    proc = sp.run(['git', 'status', '-s'], capture_output=True)
    if not proc.stdout:
        return False
    return True
