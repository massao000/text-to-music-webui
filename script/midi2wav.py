import os, glob, datetime, random, time, re
from midi2audio import FluidSynth
import wave
import numpy as np


def midi_to_wav(midi_files, wav_dir, wav_len, sf='SGM-V2.01.sf2'):
    """MIDIファイルをWAVファイルに変換する関数

    Args:
        midi_file (_type_): 変換元のMIDIファイル
        wav_dir (_type_): 保存先のWAVフォルダパス
    """
    
    # 1つだけの時にリストに変換
    if not type(midi_files) is list:
        midi_files = midi_files.split()

    if not os.path.isdir(wav_dir):
        os.mkdir(f'{wav_dir}')
        
    # name, ext = os.path.splitext(os.path.basename(sf[1]))
    # name = name.replace('.', '-')
    
    tmp_wav = [] # 音量調整前のwavリスト
    x = []
    for num, midi in enumerate(midi_files, wav_len + 1):
        print(midi)
        
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        output_wav_file = f"{wav_dir}\{num:08}-tmp.wav"
        
        tmp_wav.append(output_wav_file)
        
        flag = FluidSynth(sound_font=sf).midi_to_audio(midi, output_wav_file)

        if not flag is None:
            tmp_wav.append(output_wav_file)
        
        time.sleep(3)
    
    for i in tmp_wav:
        if os.path.isfile(i):
            x.append(volume_up(i))
    
    # 音声調整前のwavの削除
    for i in tmp_wav:
        if os.path.isfile(i):
            os.remove(i)

    print('MIDIファイルをWAVファイルに変換しました')

    return x
    # return tmp_wav
    
# wavファイルの音量の変更
def volume_up(wav_file, output_dir=None, default_volume=0.6):
    """wavファイルの音量の変更

    Args:
        wav_file (_type_): 変換先のWAVファイル
        output_dir (str, optional): 保存先. Defaults to ''.
        default_volume (float, optional): _description_. Defaults to 0.6.
    """
    if output_dir is None:
        dir_name = os.path.dirname(wav_file)
    else:
        dir_name = output_dir
        
    filename, ex = os.path.splitext(os.path.basename(wav_file))
    filename = filename.replace('-tmp', '')
    # WAVファイルを読み込む
    with wave.open(wav_file, 'rb') as wav:
        
        # チャンネル数を取得
        channels = wav.getnchannels()
        
        # サンプル幅を取得
        sample_width = wav.getsampwidth()
        
        # サンプリングレートを取得
        frame_rate = wav.getframerate()
        
        # フレーム数を取得
        num_frames = wav.getnframes()
        
        # バイト列を読み込み、NumPy配列に変換する
        wav_data = wav.readframes(num_frames)
        
        # ファイルから音声データを取得する
        wav_data = np.frombuffer(wav_data, dtype=np.int16)
        
        # チャンネル数に合わせて、配列を整形する
        wav_data = np.reshape(wav_data, (num_frames, channels))
        
        # 音声データをnumpy配列にデータ型をfloatに変換する
        wav_data = wav_data.astype(np.float32)
    
        params = wav.getparams()
    
    flag1 = False
    flag2 = False
    # 音量が0.6になる様まで音量を上げる
    while True:
        # ノーマライズして音量を計算する
        volume = np.abs(wav_data).max() / (2 ** 15)
        # print(volume)
        
        # 両方のflagがたてば保存する
        if flag1 and flag2:
            time.sleep(0.5)
            # 5. 変更されたnumpy配列をwavファイルとして書き込む
            file_name = f'{dir_name}\{filename}{ex}'
            with wave.open(file_name, 'wb') as wav:
            # with wave.open(f'output2.wav', 'wb') as wav:
                wav.setparams(params)
                wav.writeframes(wav_data.astype(np.int16))
            return file_name
        
        if default_volume >= volume:
            # numpy配列に対して音量の変更を行う
            wav_data *= 1.01
            
            flag1 = True
            
        elif default_volume <= volume:
            wav_data /= 1.01
            
            flag2 = True
            
    print('音量を調整しました')

'''
getcwd = os.getcwd()


# 環境変数の設定
path_fluidsynth = os.path.join(getcwd, r'fluidsynth\bin')

# PATH環境変数を更新します
os.environ['PATH'] = path_fluidsynth


dir_midi = os.path.join(getcwd, 'output\MIDI')
dir_wav = os.path.join(getcwd, 'output\WAV')

if not os.path.isdir(dir_midi):
    os.mkdir(dir_midi)
else:
    print('すでにMIDIフォルダは存在しています')

# 
date = datetime.datetime.now().strftime('%Y-%m-%d')
dir_wav_date = os.path.join(dir_wav, date)
if not os.path.isdir(dir_wav_date):
    os.mkdir(dir_wav_date)

midi_file = glob.glob(f'{dir_midi}\*\\')[-1]
midi_files = glob.glob(f'{midi_file}\*')
# input_midi_file = midi_files[-1]

# font.sf2
# SGM-V2.01.sf2
# yukishami20v1.sf2

sf = ['font.sf2', 'SGM-V2.01.sf2', 'yukishami20v1.sf2']

dir_name = os.path.basename(os.path.dirname(midi_files[0])) 
tmp_wav = [] # 音量調整前のwavリスト
for inp_midi_file in midi_files:
    print(inp_midi_file)
    # wabアウトプットファイル
    
    name, ext = os.path.splitext(os.path.basename(sf[1]))
    name = name.replace('.', '-')
    
    dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_wav_file = f"{dir_wav_date}\output_{dt}_{name}.wav"
    
    tmp_wav.append(output_wav_file)
    
    # MIDIファイルをWAVファイルに変換する
    midi_to_wav(f'output\MIDI\{dir_name}\{os.path.basename(inp_midi_file)}', output_wav_file, sf=sf[1])
    # midi_to_wav(f'{inp_midi_file}', output_wav_file)

    volume_up(output_wav_file)
    
time.sleep(0.3)
# 音声調整前のwavの削除
for i in tmp_wav:
    os.remove(i)
else:
    print('使用したMIDIファイルを削除しました。')
'''
