from abc import ABCMeta
import os

import requests

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_PATH, '..', 'data')


def make_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def write_file(text, destination):
    with open(destination, 'w') as f:
        f.write(text)


class BaseWriter(metaclass=ABCMeta):
    """Given a valid game id download and move XML to local file system"""
    def __init__(self, gid_url):
        self.gid_url = gid_url

    @property
    def gid(self):
        return self.gid_url.rstrip('/').split('/')[-1]

    @property
    def destination(self):
        return os.path.join(self.destination_root, self.gid + '.xml')

    @property
    def source(self):
        return os.path.join(self.gid_url, self.extension)

    def process(self):
        req = requests.get(self.source)
        if req.status_code == 200:
            write_file(req.text, self.destination)
        else:
            print(f'Non 200 status on {self.gid_url}')


class InningWriter(BaseWriter):
    destination_root = os.path.join(DATA_DIR, 'inning_all')
    extension = 'inning/inning_all.xml'
    make_folder(destination_root)


class BoxscoreWriter(BaseWriter):
    destination_root = os.path.join(DATA_DIR, 'boxscore')
    extension = 'rawboxscore.xml'
    make_folder(destination_root)


class LinescoreWriter(BaseWriter):
    destination_root = os.path.join(DATA_DIR, 'linescore')
    extension = 'linescore.xml'
    make_folder(destination_root)


class PlayersWriter(BaseWriter):
    destination_root = os.path.join(DATA_DIR, 'players')
    extension = 'players.xml'
    make_folder(destination_root)
