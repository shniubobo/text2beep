# text2beep

![Tests](https://github.com/shniubobo/text2beep/workflows/Tests/badge.svg?branch=master&event=push) [![Codecov branch](https://img.shields.io/codecov/c/github/shniubobo/text2beep/master)](https://codecov.io/gh/shniubobo/text2beep) ![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/shniubobo/text2beep/latest/master?sort=semver)

Language: 中文 | [English](README_en.md)

`text2beep` 是一个可以将纯文本形式的乐谱（目前仅支持 JSON 格式）转换成哔哔声并播放的 CLI 工具。

程序目前还在早期开发阶段，仅仅实现了最基本的合成和播放功能，之后还会陆续添加更多功能。

## 安装

本程序目前还未发布任何版本，请耐心等待第一个版本的发布。如果需要在第一个版本发布时收到通知，请点击页面右上角 Watch -> Releases Only。

在发布第一个版本之前，你可以通过这种方式安装：

```
pip install git+https://github.com/shniubobo/text2beep.git#egg=text2beep
```

## 使用方法

`text2beep` 用起来很简单，只需准备好乐谱，然后：

```
text2beep /path/to/your/sheet.json
```

程序就会读取乐谱，并根据乐谱开始合成并播放音乐。

在代码库 `examples` 目录下已经准备好了几个乐谱文件，可以用 `text2beep` 直接播放试听。

如果需要获得程序完整的选项列表，`text2beep -h` 即可。

## 创建你自己的乐谱文件

目前仅支持 JSON 格式的乐谱，将来可能会支持更多格式。

### 乐谱文件的结构

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

其中 BPM（`bpm`）和拍号（`time_signature`）用以决定乐曲播放的速度，而 `tracks` 就是乐曲的所有轨道。

如果需要将一个乐谱文件分成多个部分，或者为乐曲的不同部分指定不同的 BPM 与拍号，可以通过子乐谱（`subsheets`）实现：

```json
{
  "subsheets": [
    {
      "bpm": 120,
      "time_signature": "4/4",
      "tracks": [
        [
          "E4--- C4---"
        ],
        [
          "C4--- A3---"
        ],
        [
          "A3--- F3---"
        ],
        [
          "A2--- F2---"
        ]
      ]
    },
    {
      "bpm": 120,
      "time_signature": "2/4",
      "tracks": [
        [
          "D4--- G3---"
        ],
        [
          "B3--- E3---"
        ],
        [
          "G3--- C3---"
        ],
        [
          "G2--- C2---"
        ]
      ]
    }
  ]
}
```

将会按顺序逐一播放所有子乐谱，也可以通过 `--range` 选项指定播放范围（详见 `text2beep -h`）。

### 轨道的语法

* 每个轨道都是一个 `list`（根据 Python 的叫法）或者 `array`（根据 JSON 的叫法）。列表内部的所有字符串在程序处理时都会自动合并成一整个字符串。尽管可以把所有音符都放在一个字符串里，但还是推荐把它们放在多个字符串里来增加可读性。
* 可以在轨道中任意添加空格和 `|` 以增加可读性。程序会完全忽略它们。
* 同一个轨道中同时只能播放一个音符，而所有轨道同时播放。

### 轨道中音符的语法

* 音名必须为 `CDEFGABX` 之一，其中 `X` 用以表示休止符。
* 如果音符不是休止符，可以在音名后加上变音记号 `b` 或 `#`。
* 如果音符不是休止符，需要为其指定音高。可选的音高范围是 0 至 8。
* 需根据音名、变音记号、音高的顺序，例如 `C#4`。
* 音符默认为四分音符，如 `C4` 就是一个四分音符。
* 可以使用 `-` 为音符的时值增加 0.25，如 `C4-` 就是一个二分音符。
* 可以使用任意数量的 `-`，如 `C4---` 为一个全音符，而 `C4--` 相当于 `C4-+C4` （关于 `+` 请看下文），但这种情况下的附点音符（`C4--.`）含义模棱两可，因此不推荐使用 2 个或多于 3 个 `-`。也就是说，只使用 `-` 或 `---`。
* 可以使用 `/` 将音符的时值减半，如 `C4/` 就是一个八分音符。
* 可以使用 `.` 为音符添加附点，如 `C4.` 就是一个附点四分音符。
* `-` 和 `/` 不能同时出现在一个音符中。
* 可以使用 `+` 作为音符间的连接线（注意不是圆滑线）。

#### 一些例子：

| 音符  | 时值                           |
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

## 示例乐曲

#### [`Astronauts.json`](examples/Astronauts.json) 与 [`Astronauts.full.json`](examples/Astronauts.full.json)

* 曲名: アストロノーツ
* 原作者: [椎名もた](https://www.nicovideo.jp/watch/nm14629738)
* 编曲: [Xxoo00O00ooxX](https://www.youtube.com/watch?v=P3Ug3SY2Ctc)

#### [`Kokoronashi.json`](examples/Kokoronashi.json)

* 曲名: 心做し
* 原作者: [papiyon](https://www.nicovideo.jp/watch/sm22608740)
* 编曲: [Xxoo00O00ooxX](https://www.youtube.com/watch?v=KGOTwzoJ-iA)

#### [`Melt.json`](examples/Melt.json)

* 曲名: メルト
* 原作者: [ryo](https://www.nicovideo.jp/watch/sm1715919)
* 编曲: [Clone of Nguyễn Thanh Hoàng Hải](https://musescore.com/user/3597581/scores/1046571)

## 贡献

本项目欢迎你的贡献，详见 [`CONTRIBUTING.md`](docs/CONTRIBUTING.md)。

## 许可

本程序以 GNU GPL-3.0-or-later 许可发布。详见 [`LICENSE.txt`](LICENSE.txt)。

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
