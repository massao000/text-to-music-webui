import os, glob, datetime, random, time, re
from midi2audio import FluidSynth
import wave
import numpy as np


def abc_to_midi(abc_file_paths, midi_file_path, num):
    """ABCファイルをMIDIファイルに変換する関数

    Args:
        abc_file_paths (_type_): ABCファイルのパス
        midi_file_path (_type_): MIDIファイルの保存先
    """
    
    # 1つだけの時にリストに変換
    if not type(abc_file_paths) is list:
        abc_file_paths = abc_file_paths.split()
        
    # dir_name = os.path.basename(os.path.dirname(abc_file_paths[0]))
    # # dir_name = dir_name.replace('abc', 'midi')
    
    # os.mkdir(f"{midi_file_path}\{dir_name}")
    if not os.path.isdir(midi_file_path):
        os.mkdir(f'{midi_file_path}')
    
    new_midi_files = []
    
    for num, abc_file_path in enumerate(abc_file_paths, num + 1):
        # removal(abc_file_path)
        print(f'変換ファイル{abc_file_path}')

        # dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # MIDIファイルへの変換
        # midi_file_out = f"{midi_file_path}\{dir_name}\{dt}.mid"
        midi_file_out = f'{midi_file_path}\{num:08}.mid'

        os.system(f'abc2midi {abc_file_path} -o {midi_file_out}')
        time.sleep(3)
        
        new_midi_files.append(midi_file_out)
        
    else:
        print('ABCファイルをMIDIファイルに変換しました')
        
    return new_midi_files
    
# 無駄なものの除去
def removal(abc_file_path):
    """ABC記譜法には存在しない指定である「^（キャレット）」を削除するためのもの

    Args:
        abc_file_path (_type_): ABCファイルのパス
    """
    
    with open(abc_file_path, 'r+') as f:
        abc = f.read()
        
        pattern = r'"(.*?)"'  # ダブルクォートで囲まれた文字列をマッチする正規表現パターン
        result = re.sub(pattern, '', abc)  # ダブルクォートで囲まれた文字列を削除する
    
        f.seek(0)
        f.write(result)
        f.truncate()

'''
getcwd = os.getcwd()

# 環境変数の設定
path_abcmidi = os.path.join(getcwd, r'abc2midi')

# PATH環境変数を更新します
os.environ['PATH'] = path_abcmidi


# ファイルのパスを指定する
dir_abc = os.path.join(getcwd, 'output\ABC')
dir_midi = os.path.join(getcwd, 'output\MIDI')

if not os.path.isdir(dir_midi):
    os.mkdir(dir_midi)
else:
    print('すでにMIDIフォルダは存在しています')


# ABCファイルをファイルを取得
input_abc_file = glob.glob(f'{dir_abc}\*\\')[-1]
input_abc_files = glob.glob(f'{input_abc_file}\*')


# dir_name = [ os.path.basename(os.path.dirname(i)) for i in input_abc_file]
# # dir_name = os.path.basename(os.path.dirname(input_abc_file))

# print(dir_name)

# dir_midi_list = [ os.path.basename(i) for i in glob.glob(f'{dir_midi}\*')]

# print(dir_midi_list)



# ABCファイルをMIDIファイルに変換する
abc_to_midi(input_abc_files, dir_midi)

# 一時的なMIDIファイルを削除する
# for i in midi_files:
#     os.remove(i)
# else:
#     print('使用したMIDIファイルを削除しました。')
'''