# text2beep

Language: [中文](README.md) | English

`text2beep` is a CLI tool that converts plaintext sheet music (currently only supporting JSON format) into beeps and play them.

The tool is still in its early development with only such basic features as synthesizing and playing. More features will be added in the future.

## Installation

There hasn't been any releases yet. Please wait patiently for the first release. If you want to get notified when the first release is available, you may click "Watch -> Releases Only" at the top right corner of the page.

Before the first release, you may install by typing:

```
pip install git+https://github.com/shniubobo/text2beep.git#egg=text2beep
```

## Usage

`text2beep` is easy to use. Simply prepare your sheet, then type:

```
text2beep /path/to/your/sheet.json
```

and the program will start to read the sheet, and synthesize and play music according to it.

There are several example sheet files present in the `examples` directory. You may try them out before creating your own sheets.

For a complete option list of the tool, type `text2beep -h`.

## Creating your own sheets

Currently only JSON sheets are supported. More formats may be supported in the future.

### Structure of a sheet file

```json
{
  "bpm": 120,
  "time_signature": "4/4",
  "tracks": [
    [
      "E4--- C4--- D4--- G3---"
    ],
    [
      "C4--- A3--- B3--- E3---"
    ],
    [
      "A3--- F3--- G3--- C3---"
    ],
    [
      "A2--- F2--- G2--- C2---"
    ]
  ]
}
```

where BPM (`bpm`) and time signature (`time_signature`) are used to determine the playing speed of the song, and `tracks` are all the tracks of the song.

### Syntax of tracks

* Each track is a `list` (as is called in Python) or an `array` (as is called in JSON). All strings within the list are concatenated into a single one by the tool during runtime. Although you can put all the notes into one string, it is recommended to divide them into several ones to improve readability.
* Spaces and `|` can be added arbitrarily to improve readability. They will be completely ignored by the program.
* Notes in a track are played one by one. All tracks are played simultaneously.

### Syntax of notes in the tracks:

* The note name must be one of `CDEFGABX`, where `X` stands for rest notes.
* If a note is not a rest note, an accidental `b` or `#` may be appended to it.
* If a note is not a rest note, an octave from 0 to 8 needs to be specified.
* Name first, accidental second, octave third. For example: `C#4`.
* A note is a quarter note by default. For example, `C4` is a quarter note.
* Each `-` extends the note value by 0.25. For example, `C4-` is a half note.
* Any number of `-` may be used. For example, `C4---` is a whole note, while `C4--` is equal to `C4-+C4` (See below for `+`), although in this case the meaning of a dotted note (`C4--.`) is ambiguous, and thus the usage of two or more than three `-` is not recommended. In other words, use only `-` and `---`.
* Each `/` shortens the note value by half. For example, `C4/` is an eighth note.
* Notes can be dotted with `.`. For example, `C4.` is a dotted quarter note.
* `-` and `/` cannot be present in the same note.
* `+` can be used as a tie between notes (not a slur!).

#### Some examples:

| Note  | Value                          |
| ----- | ------------------------------ |
| X     | 0.25                           |
| X-    | 0.5                            |
| X---  | 1                              |
| X/    | 0.125                          |
| X//   | 0.0625                         |
| X.    | 0.375 (0.25 + 0.125)           |
| X..   | 0.4375 (0.25 + 0.125 + 0.0625) |
| X/.   | 0.1875 (0.125 + 0.0625)        |
| X-.   | 0.75 (0.5 + 0.25)              |
| X+X// | 0.3125 (0.25 + 0.0625)         |

## Example songs

#### [`Astronauts.json`](examples/Astronauts.json)

* Song name: アストロノーツ
* Song by: [椎名もた](https://www.nicovideo.jp/watch/nm14629738)
* Arrangement by: [Xxoo00O00ooxX](https://www.youtube.com/watch?v=P3Ug3SY2Ctc)

#### [`Kokoronashi.json`](examples/Kokoronashi.json)

* Song name: 心做し
* Song by: [papiyon](https://www.nicovideo.jp/watch/sm22608740)
* Arrangement by: [Xxoo00O00ooxX](https://www.youtube.com/watch?v=KGOTwzoJ-iA)

#### [`Melt.json`](examples/Melt.json)

* Song name: メルト
* Song by: [ryo](https://www.nicovideo.jp/watch/sm1715919)
* Arrangement by: [Clone of Nguyễn Thanh Hoàng Hải](https://musescore.com/user/3597581/scores/1046571)

## Contributing

Any contribution is much appreciated. Please see [`CONTRIBUTING_en.md`](docs/CONTRIBUTING_en.md) for details.

## License

The program is licensed under GNU GPL-3.0-or-later. Please see [`LICENSE.txt`](LICENSE.txt) for more details.

```
Copyright (C) 2020 shniubobo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
