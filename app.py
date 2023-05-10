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

def text_to_music(text, num_input, max_length, top_p, temperature, sf):
    abc_scores =  script.text2music(num_input, max_length, top_p, temperature, text)
    
    # 出力するディレクトリ
    d_now = datetime.datetime.now().strftime('%Y-%m-%d')
    t_now = datetime.datetime.now().strftime('%H%M%S')
    output_dir = os.path.join(GETCED, fr'output\text-to-music\{d_now}\{t_now}')
    
    if not os.path.isdir(output_dir):
        os.makedirs(f'{output_dir}')
    
    new_abc_files = []
    new_midi_files = []
    new_wav_files = []
    new_mp3_files = []
    
    
    # text to abc
    # abcファイル保存先
    dir_abc = os.path.join(output_dir, r'abc')
    if not os.path.isdir(dir_abc):
        os.mkdir(f'{dir_abc}')
    
    abc_files = glob.glob(f'{dir_abc}\*')
    time.sleep(3)

    for num, abc in enumerate(abc_scores, len(abc_files) + 1):
        # abc = script.removal(abc)
        
        # 編集前と編集後のabcファイルを分ける
        pattern = r'"(.*?)"'
        abc = re.sub(pattern, '', abc)
        
        if not os.path.isdir(dir_abc):
            os.mkdir(f'{dir_abc}')
    
        save_abc = f'{dir_abc}\{num:08}.abc'
        with open(save_abc, 'a') as f:
            f.write(f'{unidecode(abc)}')
            
        new_abc_files.append(save_abc)
        time.sleep(3)
        
    new_abc_files = relative_path(new_abc_files)
    
    # abc to midi
    dir_midi = os.path.join(output_dir, r'midi')
    if not os.path.isdir(dir_midi):
        os.mkdir(f'{dir_midi}')

    midi_files = glob.glob(f'{dir_midi}\*')
    
    time.sleep(2)
    new_midi_files = script.abc_to_midi(new_abc_files, dir_midi, len(midi_files))
    
    new_midi_files = relative_path(new_midi_files)
    
    # midi to wav
        
    dir_wav = os.path.join(output_dir, r'wav')
    if not os.path.isdir(dir_wav):
        os.mkdir(f'{dir_wav}')

    wav_file_len = len(glob.glob(f'{dir_wav}\*'))
    
    time.sleep(3)
    new_wav_files = script.midi_to_wav(new_midi_files, dir_wav, wav_file_len, sf)
    
    new_wav_files = relative_path(new_wav_files)
        
    # wav to mp3
    
    return random.choice(new_wav_files)

def text2abc(text, num_input, max_length, top_p, temperature):

    abc_scores =  script.text2music(num_input, max_length, top_p, temperature, text)
    
    # 出力するディレクトリ
    output_dir = os.path.join(GETCED, 'output')
    
    if not os.path.isdir(output_dir):
        os.mkdir(f'{output_dir}')

    # abcファイル保存先
    dir_abc = os.path.join(output_dir, r'text-to-abc')
    if not os.path.isdir(dir_abc):
        os.mkdir(f'{dir_abc}')
    
    dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
    dir_abc_dt = os.path.join(dir_abc, dt_now)
    abc_files = glob.glob(f'{dir_abc_dt}\*')
    time.sleep(3)

    for num, abc in enumerate(abc_scores, len(abc_files) + 1):
        # abc = script.removal(abc)
        
        pattern = r'"(.*?)"'
        abc = re.sub(pattern, '', abc)
        
        if not os.path.isdir(dir_abc_dt):
            os.mkdir(f'{dir_abc_dt}')
    
        save_abc = f'{dir_abc_dt}\{num:08}.abc'
        with open(save_abc, 'a') as f:
            f.write(f'{unidecode(abc)}')

def abc2midi(abc_file):

    # 出力するディレクトリ
    output_dir = os.path.join(GETCED, 'output')

    dir_midi = os.path.join(output_dir, r'abc-to-midi')
    if not os.path.isdir(dir_midi):
        os.mkdir(f'{dir_midi}')

    dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
    dir_midi_dt = os.path.join(dir_midi, dt_now)
    midi_files = glob.glob(f'{dir_midi_dt}\*')
    
    time.sleep(2)
    script.abc_to_midi(abc_file, dir_midi_dt, len(midi_files))

def midi2wav(midi_file, sf):

    # 出力するディレクトリ
    output_dir = os.path.join(GETCED, 'output')

    dir_wav = os.path.join(output_dir, r'midi-to-wav')
    if not os.path.isdir(dir_wav):
        os.mkdir(f'{dir_wav}')

    dt_now = datetime.datetime.now().strftime('%Y-%m-%d')
    dir_wav_dt = os.path.join(dir_wav, dt_now)
    wav_file_len = len(glob.glob(f'{dir_wav_dt}\*'))
    
    time.sleep(3)
    script.midi_to_wav(midi_file, dir_wav_dt, wav_file_len, sf)

def wav2mp3():
    pass


# UI
with gr.Blocks() as block:
    with gr.Tabs():
        with gr.TabItem("text2music"):
            text_input = gr.Textbox(label='prompt', info='song prompt', interactive=True)
            num_input = gr.Slider(1, 50, value=4, step=1, label="number of songs", interactive=True)
            max_length = gr.Slider(2, 2048, value=1024, step=2, label="max_length", interactive=True)
            top_p = gr.Slider(0.1, 0.9, value=0.9, step=0.1, label="top_p", interactive=True)
            temperature = gr.Slider(1.0, 10.0, value=1.0, step=0.1, label="temperature", interactive=True)
            # output_file = gr.CheckboxGroup(FILE_EXT, value=FILE_EXT[-1], label='create file', interactive=True)
            sound_font_input = gr.Dropdown(SOUND_FONT, label='sound font', interactive=True)
            text_button = gr.Button("run", variant="primary")
            output_audio = gr.Audio()
            
        # with gr.TabItem("abc2maid"):
        #     abcfile = gr.File(file_types=['.abc'])
        #     abc2maid_run_button = gr.Button("run", variant="primary")
        # with gr.TabItem("midi2wav"):
        #     midifile = gr.File(file_types=['.midi'])
        #     midi2wav_run_button = gr.Button("run", variant="primary")
        # with gr.TabItem("wav2mp3"):
        #     wabfile = gr.File(file_types=['.wav'])
        #     wav2mp3_run_button = gr.Button("run", variant="primary")
            
    
    text_button.click(text_to_music, inputs=[text_input, num_input, max_length, top_p, temperature, sound_font_input], outputs=output_audio)
    # abc2maid_run_button.click(abc2midi, inputs=[abcfile], outputs=abcfile)
    # midi2wav_run_button.click(midi2wav, inputs=[midifile], outputs=midifile)
    # wav2mp3_run_button.click(wav2mp3, inputs=[wabfile], outputs=wabfile)




# 起動
block.launch(
    inbrowser=True,
    quiet=True
    )
