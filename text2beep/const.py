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
from numpy import float32

__all__ = [
    'ACCIDENTALS',
    'ALIASES',
    'DTYPE',
    'FREQ_MAP',
    'NOTE_NUM',
    'NOTES',
    'NOTES_ACC',
    'NOTES_ACC_OCT',
    'OCTAVES',
    'SAMPLE_RATE',
]

# 'X' for rest notes
NOTES = list('CDEFGABX')
# 'b' for flat and '#' for sharp
ACCIDENTALS = ['b', '#']
# from '0' to '8'
OCTAVES = [str(i) for i in range(9)]

NOTES_ACC = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
# C0, C#0, D0, ..., B8
NOTES_ACC_OCT = [note+octave for octave in OCTAVES for note in NOTES_ACC]
ALIASES = {'Db': 'C#', 'D#': 'Eb', 'Gb': 'F#', 'G#': 'Ab', 'A#': 'Bb'}

# MIDI numbers of all notes, e.g. 'A4': 69
NOTE_NUM = {note: num+12 for num, note in enumerate(NOTES_ACC_OCT)}
# Frequencies of all notes, e.g. 'A4': 440.0
# Reference: https://en.wikipedia.org/wiki/Scientific_pitch_notation
FREQ_MAP = {note: 440 * 2**((num-69)/12) for note, num in NOTE_NUM.items()}

DTYPE = float32
SAMPLE_RATE = 44100
