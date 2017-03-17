from optparse import OptionParser
import os

from celery import Task

from CeleryTasks import *
from library.GidScraper import GidScraper

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

INNING_DIR = os.path.join(DATA_DIR, 'inning_all')
LINESCORE_DIR = os.path.join(DATA_DIR, 'linescore')
BOXSCORE_DIR = os.path.join(DATA_DIR, 'boxscore')
PLAYER_DIR = os.path.join(DATA_DIR, 'players')

parser = OptionParser()
parser.add_option("-y", "--year", dest="year",
                  help="Scrape input year; YYYY")
parser.add_option("-m", "--month", dest="month",
                  help="Scrape input month; YYYYMM")
parser.add_option("-d", "--day", dest="day",
                  help="Scrape input day; YYYYMMDD")
parser.add_option("-a", "--all", dest="all",
                  help=("Scrape all data from 2008 through today."
                        " Note: This could take several hours."))
parser.add_option("-p", "--procs", dest="procs",
                  help="Number of scraping processes (Be nice. :-)",
                  default=4)
parser.add_option("-k", "--keep", dest="keep",
                  help="Keep files after inserting into database",
                  default=True)

(options, args) = parser.parse_args()

if any([options.year, options.month, options.day]):
    print(options)
else:
    print('No dates to scrape provided. -h for help.')

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
