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
import os
from pathlib import Path
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

logger = logging.getLogger(__name__)


def get_version():
    version = [f'{MAJOR}.{MINOR}.{PATCH}']
    if POST is not None:
        version.append(f'.post{POST}')
    if not _is_in_git_repo():
        return ''.join(version)
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


def _is_in_git_repo():
    dot_git = Path(__file__).parent.parent / '.git'
    logger.debug(os.getcwd())
    logger.debug(f'.git: {dot_git}')
    if dot_git.exists():
        logger.debug('In a git repo')
        return True
    logger.debug('Not in a git repo')
    return False


def _get_local_changes():
    proc = sp.run(
        ['git', 'rev-list', '--tags', '--max-count=1', '--abbrev-commit'],
        stdout=sp.PIPE, stderr=sp.PIPE)
    last_tag_hash = proc.stdout.decode().strip('\n')
    proc = sp.run(['git', 'log', '-1', '--format=%h'],
                  stdout=sp.PIPE, stderr=sp.PIPE)
    last_commit_hash = proc.stdout.decode().strip('\n')
    if last_tag_hash == last_commit_hash:
        return None
    if last_tag_hash:
        commit_range = f'{last_tag_hash}..HEAD'
    else:
        commit_range = 'HEAD'
    proc = sp.run(['git', 'rev-list', commit_range, '--count'],
                  stdout=sp.PIPE, stderr=sp.PIPE)
    commits_since_last_tag = proc.stdout.decode().strip('\n')
    return commits_since_last_tag, last_commit_hash


def _is_dirty():
    logger.debug('_is_dirty called')
    proc = sp.run(['git', 'status', '-s'], stdout=sp.PIPE, stderr=sp.PIPE)
    logger.debug(f'stdout: {proc.stdout}')
    if not proc.stdout:
        return False
    return True
