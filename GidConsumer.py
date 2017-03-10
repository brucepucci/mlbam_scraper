import os

from celery import Celery

import library.XmlMovers as XmlMovers
import library.SqlWriters as SqlWriters

app = Celery('GidConsumer', broker='pyamqp://guest@localhost//')

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

INNING_DIR = os.path.join(DATA_DIR, 'inning_all')
LINESCORE_DIR = os.path.join(DATA_DIR, 'linescore')
BOXSCORE_DIR = os.path.join(DATA_DIR, 'boxscore')
PLAYER_DIR = os.path.join(DATA_DIR, 'players')

@app.task
def extract_inning(gid_url):
    return XmlMovers.InningWriter(gid_url).process()

@app.task
def extract_boxscore(gid_url):
    return XmlMovers.BoxscoreWriter(gid_url).process()

@app.task
def extract_linescore(gid_url):
    return XmlMovers.LinescoreWriter(gid_url).process()

@app.task
def extract_players(gid_url):
    return XmlMovers.PlayersWriter(gid_url).process()

@app.task
def table_inning(gid_path):
    return SqlWriters.InningWriter(gid_path).process()

@app.task
def table_rawboxscore(gid_path):
    return SqlWriters.RawBoxscoreWriter(gid_path).process()

@app.task
def table_player(gid_path):
    return SqlWriters.PlayerWriter(gid_path).process()

@app.task
def table_linescore(gid_path):
    return SqlWriters.LinescoreWriter(gid_path).process()
