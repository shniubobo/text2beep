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
from abc import ABC, abstractmethod
from itertools import islice
import json
import logging
from queue import Queue
import re
from threading import Thread

import numpy as np
import sounddevice as sd

from .const import *

__all__ = [
    'BaseSheet',
    'JSONSheet',
    'JSONSheetWithSubsheets',
    'Player',
    'Sheet',
    'Synthesizer',
    'SynthesizerBuffer',
    'SynthesizerHub',
    'Track',
]

logger = logging.getLogger(__name__)

sd.default.samplerate = SAMPLE_RATE
sd.default.channels = 1
sd.default.dtype = DTYPE


class Track:
    _note_regex = re.compile(
        r'(?:[A-G][b#]?[0-8]|X)[-/.]*(?:\+(?:[A-G][b#]?[0-8]|X)[-/.]*)*')
    _note_regex_no_value = re.compile(r'[A-G][b#]?[0-8]|X')

    def __init__(self, raw_track):
        self._notes = self._split_to_notes(raw_track)

    def __iter__(self):
        for note in self._notes:
            note_value = self._calculate_value(note)
            # Drop everything except for note names, accidentals and octaves
            note = self._note_regex_no_value.match(note).group(0)
            yield note, note_value

    def iter_slice(self, a=None, b=None, c=None):
        if b is None and c is None:
            return islice(self.__iter__(), a)
        return islice(self.__iter__(), a, b, c)

    def _split_to_notes(self, raw_track):
        # # Concise, fast, but unreadable, and silently ignores invalid notes
        # return re.findall(self._note_regex, raw_track)

        # Relatively readable, checks for invalid notes, but slow
        raw_track = list(reversed(raw_track))
        # Add an extra note so that the last note won't be missed
        raw_track.insert(0, 'C')
        note, notes = [], []
        while raw_track:
            note.append(raw_track.pop())
            # Drop all spaces and '|'
            if note[-1] in (' ', '|'):
                note.pop()
                continue
            # Append the previous note on finding a new note
            # `note[-2] != '+'` makes sure tied notes are handled correctly
            try:
                if not (note[-1] in NOTES and note[-2] != '+'
                        and len(note) > 1):
                    continue
            except IndexError:
                # Catch the exception raised by note[-2]
                continue
            notes.append(''.join(note[:-1]))
            self._ensure_note_valid(notes[-1])
            # Keep the new note for the next loop
            note = note[-1:]
        return notes

    def _ensure_note_valid(self, note):
        match = self._note_regex.match(note)
        if match is None or match.group(0) != note:
            raise ValueError(f'Invalid note: {note}')

    def _calculate_value(self, note):
        # Tied notes
        if '+' in note:
            notes = note.split('+')
            note_name = self._note_regex_no_value.match(notes[0]).group(0)
            value = 0
            for note in notes:
                if not note.startswith(note_name):
                    raise ValueError(f'Invalid note: {"+".join(notes)}')
                value += self._calculate_value(note)
            return value
        # 8th or 16th notes cannot be half or whole notes at the same time
        if '-' in note and '/' in note:
            raise ValueError(f'Invalid note: {note}')
        # Notes longer than a quarter note
        if '-' in note:
            if '.' in note:
                hyphen = note.count('-') + 1
                dot = note.count('.')
                # Dotted whole notes
                if hyphen % 4 == 0:
                    value = hyphen * (2 - 0.5**dot)
                # Dotted half notes
                elif hyphen % 2 == 0:
                    value = hyphen//4 * 4 + (hyphen % 4)*(2 - 0.5**dot)
                else:
                    # Rarely seen situations, but include them anyway
                    value = (hyphen - hyphen % 2) + (hyphen % 2)*(2 - 0.5**dot)
            else:
                value = note.count('-') + 1
        # Notes shorter than or equal to a quarter note
        else:
            value = 0.5 ** note.count('/') * (2 - 0.5 ** note.count('.'))
        # The code above assumes that the value of a quarter note is 1
        value = value / 4
        return value


class BaseSheet(ABC):
    def __init__(self, file):
        self._file = file
        self._bpm = None
        self._numerator, self._denominator = None, None
        self._tracks = None
        self._parse()

    @abstractmethod
    def _parse(self):
        pass

    @property
    def bpm(self):
        if self._bpm is None:
            raise AttributeError('Sheet not correctly initialized')
        return self._bpm

    @property
    def numerator(self):
        if self._numerator is None:
            raise AttributeError('Sheet not correctly initialized')
        return self._numerator

    @property
    def denominator(self):
        if self._denominator is None:
            raise AttributeError('Sheet not correctly initialized')
        return self._denominator

    @property
    def tracks(self):
        if self._tracks is None:
            raise AttributeError('Sheet not correctly initialized')
        return self._tracks


class JSONSheet(BaseSheet):
    def _parse(self):
        try:
            with open(self._file, 'r') as f:
                data = json.load(f)
        except TypeError:
            data = self._file
        self._bpm = data['bpm']
        time_sig = data['time_signature'].split('/')
        time_sig = tuple(map(int, time_sig))
        self._numerator, self._denominator = time_sig
        self._tracks = []
        for track in data['tracks']:
            track = Track(''.join(track))
            self._tracks.append(track)


class JSONSheetWithSubsheets(BaseSheet):
    def _parse(self):
        with open(self._file, 'r') as f:
            data = json.load(f)
        self._subsheets = \
            [JSONSheet(subsheet) for subsheet in data['subsheets']]

    def __iter__(self):
        return (subsheet for subsheet in self._subsheets)

    @property
    def bpm(self):
        return [subsheet.bpm for subsheet in self._subsheets]

    @property
    def numerator(self):
        return [subsheet.numerator for subsheet in self._subsheets]

    @property
    def denominator(self):
        return [subsheet.denominator for subsheet in self._subsheets]

    @property
    def tracks(self):
        return [subsheet.tracks for subsheet in self._subsheets]


class Sheet(BaseSheet, ABC):
    def __new__(cls, *args, **kwargs):
        try:
            return JSONSheet(*args, **kwargs)
        except KeyError:
            return JSONSheetWithSubsheets(*args, **kwargs)


class SynthesizerBuffer:
    def __init__(self, dimension, buf_duration):
        self._dimension = dimension
        self._buf_size = int(buf_duration * SAMPLE_RATE)
        self._buffer = np.zeros((dimension, self._buf_size), dtype=DTYPE)
        # To store audio data that exceeds buf_duration
        self._exceeded_buffer = {track: None for track in range(dimension)}
        # Exclusive
        self._ready_until = {track: 0 for track in range(dimension)}

    def append(self, track, data):
        if self.is_track_full(track):
            raise ValueError('Buffer of the track already full')
        new_buf_size = len(data)
        last_end = self._ready_until[track]
        buf_size_avail = self._size_needed_before_ready(track)
        if new_buf_size <= buf_size_avail:
            self._buffer[track, last_end:last_end+new_buf_size] = data
            self._move_forward_ready_until(track, new_buf_size)
        else:
            self._buffer[track, last_end:] = data[:buf_size_avail]
            self._move_forward_ready_until(track, buf_size_avail)
            self._exceeded_buffer[track] = data[buf_size_avail:]
        return self.is_track_full(track)

    def flush(self):
        for track in range(self._dimension):
            if not self.is_track_full(track):
                raise ValueError('Not ready to be flushed')
        result = self._mix_all_tracks()
        self._reset_ready_until()
        self._take_exceeded_buffer_after_flushing()
        return result

    def force_flush(self):
        try:
            return self.flush()
        except ValueError:
            pass
        for track in range(self._dimension):
            zero_since = self._size_needed_before_ready(track)
            self._buffer[track, -zero_since:].fill(0)
        result = np.sum(self._buffer, axis=0, dtype=DTYPE)
        result = np.trim_zeros(result, 'b')
        self._reset_ready_until()
        self._take_exceeded_buffer_after_flushing()
        return result

    def is_track_full(self, track):
        full = self._exceeded_buffer[track] is not None \
               or self._size_needed_before_ready(track) == 0
        return full

    def _size_needed_before_ready(self, track):
        return self._buf_size - self._ready_until[track]

    def _mix_all_tracks(self):
        return np.sum(self._buffer, axis=0, dtype=DTYPE)

    def _reset_ready_until(self):
        self._ready_until = {track: 0 for track in range(self._dimension)}

    def _move_forward_ready_until(self, track, length):
        new_value = self._ready_until[track] + length
        error_msg = (f'Got self._ready_until[{track}] = {new_value}; '
                     f'expected to be no greater than {self._buf_size}')
        assert new_value <= self._buf_size, error_msg
        self._ready_until[track] = new_value

    def _take_exceeded_buffer_after_flushing(self):
        for track, ex_buffer in self._exceeded_buffer.items():
            if ex_buffer is not None:
                exceeded_size = np.shape(ex_buffer)[0]
                if exceeded_size <= self._buf_size:
                    # _buffer can take the whole _exceeded_buffer
                    self._buffer[track, :exceeded_size] = ex_buffer
                    self._exceeded_buffer[track] = None
                    self._move_forward_ready_until(track, exceeded_size)
                else:
                    # _buffer cannot take the whole _exceeded_buffer
                    self._buffer[track, :] = ex_buffer[:self._buf_size]
                    self._exceeded_buffer[track] = ex_buffer[self._buf_size:]
                    self._move_forward_ready_until(track, self._buf_size)

    @property
    def is_empty(self):
        for size in self._ready_until.values():
            if size != 0:
                return False
        return True


class Synthesizer:
    def __init__(self, sheet):
        self._sheet = sheet
        self._track_count = len(sheet.tracks)
        # In seconds
        beat_duration = 1 / sheet.bpm * 60
        bar_duration = beat_duration * sheet.numerator
        self._buffer = SynthesizerBuffer(self._track_count, bar_duration)
        self._queue = Queue(1)
        self._note_value_total = \
            {track: 0 for track in range(self._track_count)}
        self._started, self._finished = False, False

    def synthesize(self):
        try:
            self._start_to_synthesize_and_serve()
            self._serve_remaining_buffer_before_stopping()
            self._warn_not_matching_value()
        finally:
            self._serve_end_of_stream()
            self._finished = True

    def _start_to_synthesize_and_serve(self):
        self._started = True
        track_iters = self._get_track_iterators()
        # Synthesize one track until its buffer is full, and then synthesize
        # the next track. When all tracks' buffer is full, serve the buffer
        # so that the player can consume it.
        while True:
            for idx, track_iter in enumerate(track_iters):
                if self._buffer.is_track_full(idx):
                    continue
                while True:
                    try:
                        note = next(track_iter)
                    except StopIteration:
                        logger.debug(f'StopIteration at track {idx}')
                        if idx + 1 < self._track_count:
                            break
                        return
                    self._increase_track_note_value(idx, note[1])
                    logger.debug(f'Synthesizing {note} (track {idx})')
                    audio = self._synthesize_note(note)
                    full = self._buffer.append(idx, audio)
                    if full:
                        break
            logger.debug('Serving buffer')
            self._serve_and_wait(self._buffer.flush())
            logger.debug('-' * 50)

    def _get_track_iterators(self):
        return [iter(self._sheet.tracks[idx])
                for idx in range(len(self._sheet.tracks))]

    def _synthesize_note(self, note):
        note, note_value = note
        beats_per_value = self._sheet.denominator
        beat_duration = 1 / self._sheet.bpm * 60
        note_duration = note_value * beats_per_value * beat_duration
        sample_quantity = int(note_duration * SAMPLE_RATE)
        samples_x = np.linspace(0, note_duration, sample_quantity, False)
        freq = self._note_to_frequency(note)
        volume = 0.07
        fade = 1 / np.exp(samples_x)
        audio = volume * np.sin(2 * np.pi * freq * samples_x) * fade
        audio = audio.astype(DTYPE)
        return audio

    def _note_to_frequency(self, note):
        if note == 'X':
            return 0
        try:
            return FREQ_MAP[note]
        except KeyError:
            note = self._resolve_note_alias(note)
            return FREQ_MAP[note]

    @staticmethod
    def _resolve_note_alias(note):
        note_name_acc = note[:-1]
        note_oct = note[-1:]
        return ALIASES[note_name_acc] + note_oct

    def _serve_and_wait(self, to_serve):
        self._queue.put(to_serve)
        self._queue.join()

    def _serve_remaining_buffer_before_stopping(self):
        if not self._buffer.is_empty:
            # logger.warning('Incomplete bar found')
            logger.debug('Serving the remainder of buffer')
            self._serve_and_wait(self._buffer.force_flush())
            logger.debug('-' * 50)

    def _serve_end_of_stream(self):
        logger.debug('Serving end of stream')
        self._queue.put(None)

    def _warn_not_matching_value(self):
        track_zero_value = self._note_value_total[0]
        for value in self._note_value_total.values():
            if value != track_zero_value:
                break
        else:
            return
        logger.warning('Total note value of each track not matching!')
        for track, value in self._note_value_total.items():
            logger.warning(f'Track {track}: {value}')

    def _increase_track_note_value(self, track, value):
        self._note_value_total[track] += value

    @property
    def queue(self):
        return self._queue

    @property
    def started(self):
        return self._started

    @property
    def finished(self):
        return self._finished


class SynthesizerHub:
    def __init__(self, *sheets):
        self._sheets = list(sheets)
        self._synthesizers = [Synthesizer(sheet) for sheet in self._sheets]
        self._queue = Queue(1)

    def synthesize(self):
        try:
            self._start_synthesizers_and_proxy_queues()
        finally:
            self._serve_end_of_stream()
            self._drain_all_synthesizers()

    def _start_synthesizers_and_proxy_queues(self):
        for idx, synthesizer in enumerate(self._synthesizers):
            thread = Thread(target=synthesizer.synthesize,
                            name=f'Synthesizer-{idx}')
            thread.start()
            while True:
                item = self._consume_one_item_from_queue(synthesizer)
                if item is None:
                    break
                self._serve_and_wait(item)
            thread.join()

    @staticmethod
    def _consume_one_item_from_queue(synthesizer):
        item = synthesizer.queue.get()
        synthesizer.queue.task_done()
        return item

    def _serve_and_wait(self, to_serve):
        self._queue.put(to_serve)
        self._queue.join()

    def _serve_end_of_stream(self):
        logger.debug('Serving end of stream')
        self._queue.put(None)

    def _drain_all_synthesizers(self):
        for idx, synthesizer in enumerate(self._synthesizers):
            if not synthesizer.started or synthesizer.finished:
                continue
            logger.debug(f'Synthesizer {idx} has not finished. Draining it')
            while True:
                result = self._consume_one_item_from_queue(synthesizer)
                if result is None:
                    break

    @property
    def queue(self):
        return self._queue


class Player:
    def __init__(self, sheet):
        self._thread = _PlayerThread()
        try:
            self._synthesizer = Synthesizer(sheet)
        except TypeError:
            self._synthesizer = SynthesizerHub(*sheet)
        self._thread.connect_queue(self._synthesizer.queue)

    def play(self):
        self._thread.start()
        self._synthesizer.synthesize()
        self._thread.join()


class _PlayerThread(Thread):
    def __init__(self):
        super().__init__(name='_PlayerThread')
        self._queue = None

    def run(self):
        assert self._queue is not None
        with sd.OutputStream() as stream:
            while True:
                audio = self._queue.get()
                self._queue.task_done()
                if audio is None:
                    logger.debug('End of stream')
                    break
                sample_count = len(audio)
                logger.debug(f'Got {sample_count} samples '
                             f'({sample_count/SAMPLE_RATE:.3f}s)')
                stream.write(audio)

    def connect_queue(self, queue):
        self._queue = queue
