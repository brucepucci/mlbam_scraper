import os

from celery import Task

from library.CeleryTasks import *
from library.GidScraper import GidScraper

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

INNING_DIR = os.path.join(DATA_DIR, 'inning_all')
LINESCORE_DIR = os.path.join(DATA_DIR, 'linescore')
BOXSCORE_DIR = os.path.join(DATA_DIR, 'boxscore')
PLAYER_DIR = os.path.join(DATA_DIR, 'players')

for gid_url in GidScraper().get_gids():
    gid_file = gid_url.split('/')[-2] + '.xml'

    extract_inning.apply_async(args=[gid_url], link=table_inning.s(
        gid_path=os.path.join(INNING_DIR, gid_file)))
    extract_boxscore.apply_async(args=[gid_url], link=table_boxscore.s(
        gid_path=os.path.join(BOXSCORE_DIR, gid_file)))
    extract_linescore.apply_async(args=[gid_url], link=table_linescore.s(
        gid_path=os.path.join(LINESCORE_DIR, gid_file)))
    extract_player.apply_async(args=[gid_url], link=table_player.s(
        gid_path=os.path.join(PLAYER_DIR, gid_file)))

