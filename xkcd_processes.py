import requests

from random import randint
from os import makedirs
from os.path import join as join_path
from os.path import splitext


def download_image(url, directory, filename):
    response = requests.get(url)
    response.raise_for_status()
    makedirs(directory, exist_ok=True)
    path = join_path(directory, filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def return_extension(url):
    return url.split('/')[-1].split('.')[-1]


def fetch_comics(id_comics):
    url = f'https://xkcd.com/{id_comics}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['img'], response.json()['alt'], id_comics


def fetch_last():
    url = f'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def fetch_random_comics():
    last_comics = fetch_last()
    return fetch_comics(randint(1, last_comics))


def download_random_comics(directory):
    url, message, id_comics = fetch_random_comics()
    filename = f'xkcd_{id_comics}{splitext(url)[1]}'
    file_path = download_image(url, directory, filename)
    return [file_path, message]


if __name__ == '__main__':
    print(download_random_comics)

