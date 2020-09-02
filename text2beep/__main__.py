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
import argparse
import logging
import sys

from .core import *
from .version import get_version

logging.captureWarnings(True)
logger = logging.getLogger(__name__)


def _get_args():
    description = 'A CLI tool that converts plaintext sheet music to beeps.'
    parser = argparse.ArgumentParser(prog='text2beep', description=description,
                                     add_help=False)
    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                        help='Suppress all logs. Overwrite --verbose.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help='Enable verbose logging (default to off).')
    parser.add_argument('-V', '--version', action='store_true', dest='version',
                        help='Print the version number and exit.')
    parser.add_argument('-r', '--range', action='store', dest='range',
                        help='The range of subsheets to be played, in the '
                             'format of "start,end" (quotes not required). If '
                             'not specified, all subsheets will be played.')
    if not ('-V' in sys.argv or '--version' in sys.argv):
        parser.add_argument('FILE', help='The file to be converted to beeps.')
    return vars(parser.parse_args())


def _parse_args(args):
    if args['quiet']:
        logging.basicConfig(level=60)
    elif args['verbose']:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s:%(name)s:%(threadName)s:'
                                   '%(lineno)d:%(message)s')
    else:
        logging.basicConfig(level=logging.INFO)
    if args['version']:
        print(f'text2beep {get_version()}')
        sys.exit(0)
    if args['range'] is None:
        play_range = None
    else:
        play_range = args['range'].split(',')
        play_range = map(int, play_range)
        play_range = tuple(play_range)
    return args['FILE'], play_range


def main():
    args = _get_args()
    file, play_range = _parse_args(args)

    sheet = Sheet(file)
    player = Player(sheet, play_range)
    logger.info(f'Playing {file}')
    player.play()


if __name__ == '__main__':
    main()
