from abc import ABCMeta, abstractmethod
import os

import MySQLdb

import library.XmlParsers as XmlParsers

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(BASE_PATH, '..', 'sql')
INSERT_SQL_DIR = os.path.join(SQL_DIR, 'insert')


def read_query(query_path):
    with open(query_path, 'r') as query_file:
        return(' '.join(query_file.read().split()))


def write_row(query, values):
    con = MySQLdb.connect(user='root', db='mlbam')
    cur = con.cursor()
    try:
        cur.execute(query.format(**values))
        con.commit()
    except:
        con.rollback()
        raise
    cur.close()
    con.close()


class BaseWriter(metaclass=ABCMeta):
    def __init__(self, source_file):
        self.source_file = source_file

    @abstractmethod
    def process(self):
        pass


class InningWriter(BaseWriter):
    insert_atbat_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                 'inning',
                                                 'insert_atbat.sql'))
    insert_pitch_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                 'inning',\
                                                 'insert_pitch.sql'))

    def process(self):
        for table, vals in XmlParsers.InningParser(self.source_file).process():
            if table == 'atbat':
                write_row(self.insert_atbat_query, vals)
            elif table == 'pitch':
                write_row(self.insert_pitch_query, vals)
            else:
                pass


class RawBoxscoreWriter(BaseWriter):
    insert_batter_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                  'rawboxscore',
                                                  'insert_batter.sql'))
    insert_boxscore_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                    'rawboxscore',
                                                    'insert_boxscore.sql'))
    insert_inning_line_score_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                             'rawboxscore',
                                                             'insert_inning_line_score.sql'))
    insert_linescore_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                     'rawboxscore',
                                                     'insert_linescore.sql'))
    insert_pitcher_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                   'rawboxscore',
                                                   'insert_pitcher.sql'))
    insert_team_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                'rawboxscore',
                                                'insert_team.sql'))
    insert_umpire_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                  'rawboxscore',
                                                  'insert_umpire.sql'))

    def process(self):
        for table, vals in XmlParsers.RawBoxscoreParser(self.source_file).process():
            if table == 'batter':
                write_row(self.insert_batter_query, vals)
            elif table == 'boxscore':
                write_row(self.insert_boxscore_query, vals)
            elif table == 'inning_line_score':
                write_row(self.insert_inning_line_score_query, vals)
            elif table == 'linescore':
                write_row(self.insert_linescore_query, vals)
            elif table == 'pitcher':
                write_row(self.insert_pitcher_query, vals)
            elif table == 'team':
                write_row(self.insert_team_query, vals)
            elif table == 'umpire':
                write_row(self.insert_umpire_query, vals)
            else:
                pass

if __name__ == '__main__':
    RawBoxscoreWriter('/Users/bruce/Projects/mlbam_scraper/data/mlbam_2016/boxscore/gid_2016_04_03_nynmlb_kcamlb_1.xml').process()
