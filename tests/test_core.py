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
from inspect import isgenerator
from pathlib import Path
from queue import Queue

import numpy as np
import pytest

from text2beep.core import *
from text2beep.const import DTYPE, NOTE_NUM, SAMPLE_RATE


@pytest.fixture(name='sheet')
def fixture_sheet():
    sheet_path = Path(__file__).parent / 'test_sheet.json'
    return Sheet(sheet_path)


def test_track():
    track = Track('C4D4E4F4G4A4B4')
    assert isgenerator(iter(track))
    assert len(list(track)) == 7
    for note, note_value in track:
        assert note in NOTE_NUM
        assert note_value == 0.25
    _test_track_iter_range(track)
    _test_track_exception_on_invalid_note()
    _test_track_note_values()


def _test_track_iter_range(track):
    assert len(list(track.iter_slice())) == 7
    assert len(list(track.iter_slice(3))) == 3
    assert len(list(track.iter_slice(None, 5))) == 5
    assert len(list(track.iter_slice(None, None, 2))) == 4
    assert len(list(track.iter_slice(1, 3))) == 2
    assert len(list(track.iter_slice(1, None, 2))) == 3
    assert len(list(track.iter_slice(None, 5, 2))) == 3
    assert len(list(track.iter_slice(1, 5, 2))) == 2


def _test_track_exception_on_invalid_note():
    with pytest.raises(ValueError) as exc_info:
        Track('An invalid note')
    assert exc_info.value.args[0] == 'Invalid note: Aninvalidnote'

    another_invalid_note = 'C4-/'
    with pytest.raises(ValueError) as exc_info:
        list(Track(another_invalid_note))
    assert exc_info.value.args[0] == f'Invalid note: {another_invalid_note}'

    yet_another = 'C4+C5'
    with pytest.raises(ValueError) as exc_info:
        list(Track(yet_another))
    assert exc_info.value.args[0] == f'Invalid note: {yet_another}'


def _test_track_note_values():
    notes = 'C4+C4 C4--- C4- C4 C4---. C4--. C4-. C4. C4/ C4/.'
    note_values = [0.5, 1, 0.5, 0.25, 1.5, 0.875, 0.75, 0.375, 0.125, 0.1875]
    track = Track(notes)
    for note, note_value in zip(track, note_values):
        assert note[1] == note_value


class NotProperlyInitiatedSheet(BaseSheet):
    def _parse(self):
        pass


def test_base_sheet():
    with pytest.raises(TypeError):
        _ = BaseSheet('file')

    sheet = NotProperlyInitiatedSheet('file')
    with pytest.raises(AttributeError):
        _ = sheet.bpm
    with pytest.raises(AttributeError):
        _ = sheet.numerator
    with pytest.raises(AttributeError):
        _ = sheet.denominator
    with pytest.raises(AttributeError):
        _ = sheet.tracks


def test_json_sheet(sheet):
    assert sheet.bpm == 120
    assert sheet.numerator == 4
    assert sheet.denominator == 4
    assert isinstance(sheet.tracks, list)
    assert len(sheet.tracks) == 4
    for track in sheet.tracks:
        assert isinstance(track, Track)


def test_sheet(sheet):
    assert isinstance(sheet, JSONSheet)
    assert isinstance(sheet, BaseSheet)
    assert not isinstance(sheet, Sheet)


def test_synthesizer_buffer():
    buffer = SynthesizerBuffer(2, 1)
    assert buffer.is_empty
    assert not buffer.append(0, np.ones(100, dtype=DTYPE))
    assert not buffer.is_empty
    assert buffer.append(0, np.ones(SAMPLE_RATE, dtype=DTYPE))
    assert buffer.append(1, np.ones(SAMPLE_RATE, dtype=DTYPE))
    with pytest.raises(ValueError):
        buffer.append(0, np.ones(100, dtype=DTYPE))
    with pytest.raises(ValueError):
        buffer.append(1, np.ones(100, dtype=DTYPE))
    np.testing.assert_equal(buffer.flush(),
                            np.full(SAMPLE_RATE, 2, dtype=DTYPE))
    with pytest.raises(ValueError):
        buffer.flush()
    np.testing.assert_equal(buffer.force_flush(), np.ones(100, dtype=DTYPE))
    assert buffer.append(0, np.ones(int(SAMPLE_RATE*2.5), dtype=DTYPE))
    assert buffer.append(1, np.ones(int(SAMPLE_RATE*2.5), dtype=DTYPE))
    buffer.flush()
    assert buffer.flush().shape == (SAMPLE_RATE,)
    assert buffer.force_flush().shape == (SAMPLE_RATE/2,)


class DummyPlayer:
    def __init__(self):
        self._synthesizer = None
        self._queue = None

    def connect(self, synthesizer):
        self._synthesizer = synthesizer
        self._queue = self._synthesizer.queue

    def play(self):
        self._synthesizer.start()
        while True:
            audio = self._queue.get()
            self._queue.task_done()
            if audio is None:
                yield 'End of stream'
                break
            yield audio


def test_synthesizer(sheet, caplog):
    synthesizer = Synthesizer(sheet)
    player = DummyPlayer()
    player.connect(synthesizer)
    audio = list(player.play())
    assert audio[-1] == 'End of stream'
    audio = np.concatenate(audio[:-1])
    beat_duration = 1 / sheet.bpm * 60
    bar_duration = int(beat_duration * sheet.numerator)
    assert audio.size == 2.5 * bar_duration * SAMPLE_RATE
    assert 'not matching!' in caplog.text
    assert 'Track 0: 2.5' in caplog.text
    assert 'Track 1: 2.5' in caplog.text
    assert 'Track 2: 2.5' in caplog.text
    assert 'Track 3: 2.0' in caplog.text
    _test_synthesizer_keyboard_interrupt(sheet)
    _test_synthesizer_matching_note_value(caplog)


def _test_synthesizer_keyboard_interrupt(sheet):
    synthesizer = Synthesizer(sheet)
    synthesizer.start()
    synthesizer.keyboard_interrupt.set()
    synthesizer.queue.get()
    synthesizer.queue.task_done()
    end_of_stream = synthesizer.queue.get()
    assert end_of_stream is None
    synthesizer.join()


def _test_synthesizer_matching_note_value(caplog):
    caplog.clear()
    sheet = JSONSheet(Path('examples/Am-F-G-C.json'))
    synthesizer = Synthesizer(sheet)
    player = DummyPlayer()
    player.connect(synthesizer)
    player.play()
    assert 'not matching!' not in caplog.text


class DummyOutputStream:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def write(audio):
        print(audio)


class DummySynthesizer:
    def __init__(self, _=None):
        self.queue = Queue(1)
        self.keyboard_interrupt = DummyEvent()
        self.alive = True

    def start(self):
        pass

    def is_alive(self):
        return self.alive

    def join(self, _):
        dummy_audio = np.ones(SAMPLE_RATE * 3, dtype=DTYPE)
        for _ in range(2):
            self.queue.put(dummy_audio)
            self.queue.join()
        try:
            raise KeyboardInterrupt
        finally:
            self.queue.put(None)
            self.alive = False


class DummyEvent:
    def set(self):
        pass


def test_player(sheet, monkeypatch, caplog):
    player = Player(sheet)
    with monkeypatch.context() as m:
        m.setattr('sounddevice.OutputStream', DummyOutputStream)
        player.play()
        _test_player_keyboard_interrupt(monkeypatch, caplog)


def _test_player_keyboard_interrupt(monkeypatch, caplog):
    with monkeypatch.context() as m:
        m.setattr('text2beep.core.Synthesizer', DummySynthesizer)
        player = Player(None)
        player.play()
        assert 'Got KeyboardInterrupt' in caplog.text
