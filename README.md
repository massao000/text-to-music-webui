# text-to-music-webui

Windows

<!-- 
以下のものを利用します
- ffmpeg
    - https://www.ffmpeg.org/download.html
- FluidSynth
    - https://github.com/FluidSynth/fluidsynth/releases
- abcmidi
    - [github](https://github.com/sshlien/abcmidi)
    - [オリジナル](https://abc.sourceforge.net/abcMIDI/original/)
    - [DLサイト](https://abcplus.sourceforge.net/#abcmidi)
    - [インストール方法](https://mahoroba.logical-arts.jp/archives/1865)
-->

## setting

### ffmpeg

[DLサイト](https://github.com/BtbN/FFmpeg-Builds/releases)からどちらかダウンロードしてください
- ffmpeg-master-latest-win64-gpl.zip
- ffmpeg-master-latest-win64-gpl-shared.zip

解凍したZIPファイル内のファイルを`ffmpegフォルダ`すべて移動させます。

```
text-to-music-webui-main
├─ffmpeg
│  └─bin
```

### FluidSynth

[DLサイト](https://github.com/FluidSynth/fluidsynth/releases)からどちらかダウンロードしてください。

解凍したZIPファイル内のファイルを`fluidsynthフォルダ`すべて移動させます。

```
text-to-music-webui-main
├─fluidsynth
│  └─bin
```

### abcmidi

すでに入っているのでダウンロードは必要ない

[DLサイト](https://abcplus.sourceforge.net/#abcmidi)

<!--
[DLサイト](https://abcplus.sourceforge.net/#abcmidi)からどちらかダウンロードしてください。

解凍したZIPファイル内のファイルを`abc2midiフォルダ`に移動させます。

```
text-to-music-webui-main
├─abc2midi
```
-->

環境
```
pip install -r requirements.txt
```
