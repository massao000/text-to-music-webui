from mutagen.easyid3 import EasyID3
import datetime


x = r'output_file.mp3'
# x = r'output\WAV\2023-04-12\output-20230412212117-up.wav'

# audio = mutagen.File(x)

audio = EasyID3(x)
# print(t)

# タグ情報を表示する
# print(audio.tags)
print(audio)

# ID3タグが存在しない場合は新しいタグを作成する
# if not audio:
#     audio.add_tags()
    
audio['title'] = 'タイトル'  # 曲のタイトル
# audio.tags['artist'] = 'アーティスト'  # アーティスト名
# audio.tags['date'] = datetime.datetime.now().strftime('%Y-%m-%d')  # 発売年
# audio.tags['genre'] = 'ロック'  # ジャンル
# audio.tags['tracknumber'] = '5'  # トラック番号
    
# audio.save()

print(audio)