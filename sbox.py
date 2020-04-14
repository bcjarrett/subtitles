import os
import glob
import hashlib
import requests

# Settings
movie_folder = r'C:\Test'
video_extensions = ['mkv', 'avi', 'mp4']
languages = ['en', 'us', 'eng']
headers = {"user-agent": "SubDB/1.0 (SubtitleUpdate/0.1; https://github.com/bcjarrett)"}


def get_video_files(dir_):
    movie_paths = []
    for ext in video_extensions:
        movie_paths += glob.glob(f'{dir_}\\**\\*.{ext}', recursive=True)
    return movie_paths


def get_hash(name):
    read_size = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(read_size)
        f.seek(-read_size, os.SEEK_END)
        data += f.read(read_size)
    return hashlib.md5(data).hexdigest()


def create_url(file_path):
    return f'http://api.thesubdb.com/?action=download&hash={get_hash(file_path)}&language={",".join(languages)}'


def download(data, file_path):
    filename = '.'.join(file_path.split('.')[:-1])
    with open(filename + ".srt", 'wb') as f:
        f.write(data)
    f.close()


def get_subtitle(file_path):
    url = create_url(file_path)
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        data = req.content
        download(data, file_path)
    else:
        print(f'Error: {req.status_code}')
        print(f'{req.content}')


if __name__ == '__main__':
    movies = get_video_files(movie_folder)
    for movie in movies:
        get_subtitle(movie)
