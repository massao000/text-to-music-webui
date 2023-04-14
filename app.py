import gradio as gr
import os, glob, datetime, random, time, re
from midi2audio import FluidSynth
import wave
import numpy as np
import script
from unidecode import unidecode

GETCED = os.getcwd()

FILE_EXT = ('ABC', 'MIDE', 'WAV', 'MP3')
SOUND_FONT = glob.glob(f'.\soundFont\*.sf2')

# 環境変数の設定
path_fluidsynth = os.path.join(GETCED, r'fluidsynth\bin')
path_abcmidi = os.path.join(GETCED, r'abc2midi')
path_ffmpeg = os.path.join(GETCED, r'ffmpeg\bin')

new_paths = ';'.join([path_fluidsynth, path_abcmidi, path_ffmpeg])

# PATH環境変数を更新します
os.environ['PATH'] = new_paths

# 相対パスに変換
def relative_path(path):
    
    return [ os.path.relpath(i, GETCED) for i in path ]

def text_to_music(text, num_input, max_length, top_p, temperature, file, sf):
    abc_scores =  script.text2music(num_input, max_length, top_p, temperature, text)
    
    path = os.getcwd()
    # 出力するディレクトリ
    output_dir = os.path.join(path, 'output')
    
    if not os.path.isdir(output_dir):
        os.mkdir(f'{output_dir}')
    
    new_abc_files = []
    new_midi_files = []
    new_wav_files = []
    new_mp3_files = []
    
    
    # text to abc
    if  FILE_EXT[0] in file:
        print(FILE_EXT[0])
        # abcファイル保存先
        dir_abc = os.path.join(output_dir, r'text-to-abc')
        if not os.path.isdir(dir_abc):
            os.mkdir(f'{dir_abc}')
        
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
        dir_abc_dt = os.path.join(dir_abc, dt_now)
        abc_files = glob.glob(f'{dir_abc_dt}\*')
        time.sleep(3)
        # dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        for num, abc in enumerate(abc_scores, len(abc_files) + 1):
            # abc = script.removal(abc)
            
            pattern = r'"(.*?)"'
            abc = re.sub(pattern, '', abc)
            
            # dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
            # dir_abc_dt = os.path.join(dir_abc, dt_now)
            # abc_file_len = len(glob.glob(f'{dir_abc_dt}\*'))
            
            if not os.path.isdir(dir_abc_dt):
                os.mkdir(f'{dir_abc_dt}')
        
            save_abc = f'{dir_abc_dt}\{num:08}.abc'
            with open(save_abc, 'a') as f:
                f.write(f'{unidecode(abc)}')
                
            new_abc_files.append(save_abc)
            time.sleep(3)
            
        new_abc_files = relative_path(new_abc_files)
    
    # abc to midi
    if  FILE_EXT[1] in file:
        print(FILE_EXT[1])
        
        dir_midi = os.path.join(output_dir, r'abc-to-midi')
        if not os.path.isdir(dir_midi):
            os.mkdir(f'{dir_midi}')

        dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
        dir_midi_dt = os.path.join(dir_midi, dt_now)
        midi_files = glob.glob(f'{dir_midi_dt}\*')
        
        time.sleep(2)
        new_midi_files = script.abc_to_midi(new_abc_files, dir_midi_dt, len(midi_files))
        
        # 変換できなっ方ものの削除
        # comparison = list(set(new_midi_files) ^ set(midi_files))
        
        # print(f'確認：{midi_files}')
        # print(f'確認：{new_midi_files}')
        # print(f'確認：{comparison}')
        
        # for num, i in enumerate(new_midi_files):
        #     if i in comparison:
        #         new_midi_files.pop(num)

        
        new_midi_files = relative_path(new_midi_files)
    
    # midi to wav
    if  FILE_EXT[2] in file:
        print(FILE_EXT[2])
        
        dir_wav = os.path.join(output_dir, r'midi-to-wav')
        if not os.path.isdir(dir_wav):
            os.mkdir(f'{dir_wav}')

        dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
        dir_wav_dt = os.path.join(dir_wav, dt_now)
        wav_file_len = len(glob.glob(f'{dir_wav_dt}\*'))
        
        time.sleep(3)
        new_wav_files = script.midi_to_wav(new_midi_files, dir_wav_dt, wav_file_len, sf)
        
        new_wav_files = relative_path(new_wav_files)
        
    # wav to mp3
    if  FILE_EXT[3] in file:
        print(FILE_EXT[3])
                
                
    # abcからmidiにこの時の変換しといてい
    # さらにmidiからwavにしてもいいかもしれない
    # print(text, num_input, max_length, top_p, temperature, file, FILE_EXT)
    # print(new_abc_files)
    # print(new_midi_files)
    # print(new_wav_files)
    
    return random.choice(new_wav_files)

def get_time():
    return datetime.datetime.now().time()

# UI
with gr.Blocks() as block:
    with gr.Tabs():
        with gr.TabItem("text2music"):
            text_input = gr.Textbox(label='prompt')
            num_input = gr.Slider(1, 50, value=4, step=1, label="曲数", interactive=True)
            max_length = gr.Slider(2, 2048, value=1024, step=2, label="max_length", interactive=True)
            top_p = gr.Slider(0.1, 0.9, value=0.9, step=0.1, label="top_p", interactive=True)
            temperature = gr.Slider(1.0, 10.0, value=1.0, step=0.1, label="temperature", interactive=True)
            output_file = gr.CheckboxGroup(FILE_EXT, value=FILE_EXT[-1], label='create file', interactive=True)
            sound_font_input = gr.Dropdown(SOUND_FONT, label='sound font', interactive=True)
            text_button = gr.Button("Flip")
            output_audio = gr.Audio()
            
            # text_button = gr.Button("Flip")
        with gr.TabItem("abc2maid"):
            pass
        with gr.TabItem("midi2wav"):
            pass
        with gr.TabItem("wav2mp3"):
            pass
        
    # dt = gr.Textbox(label="Current time")
    # block.load(get_time, inputs=None, outputs=dt)
    
    text_button.click(text_to_music, inputs=[text_input, num_input, max_length, top_p, temperature, output_file, sound_font_input], outputs=output_audio)
    # text_button.click(text_to_music, inputs=[text_input, num_input, max_length, top_p, temperature])
    

# 起動
block.launch()