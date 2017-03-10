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
    insert_runner_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                  'inning',\
                                                  'insert_runner.sql'))

    def process(self):
        for table, vals in XmlParsers.InningParser(self.source_file).process():
            if table == 'atbat':
                write_row(self.insert_atbat_query, vals)
            elif table == 'pitch':
                write_row(self.insert_pitch_query, vals)
            elif table == 'runner':
                write_row(self.insert_runner_query, vals)
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


class LinescoreWriter(BaseWriter):
    insert_inningscore_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                 'linescore',
                                                 'insert_inningscore.sql'))
    insert_game_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                 'linescore',\
                                                 'insert_game.sql'))

    def process(self):
        for table, vals in XmlParsers.LinescoreParser(self.source_file).process():
            if table == 'game':
                write_row(self.insert_game_query, vals)
            elif table == 'inningscore':
                write_row(self.insert_inningscore_query, vals)
            else:
                pass


class PlayerWriter(BaseWriter):
    insert_player_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                 'player',
                                                 'insert_player.sql'))
    insert_coach_query = read_query(os.path.join(INSERT_SQL_DIR,
                                                 'player',\
                                                 'insert_coach.sql'))

    def process(self):
        for table, vals in XmlParsers.PlayerParser(self.source_file).process():
            if table == 'player':
                write_row(self.insert_player_query, vals)
            elif table == 'coach':
                write_row(self.insert_coach_query, vals)
            else:
                pass

