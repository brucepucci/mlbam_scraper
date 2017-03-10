from abc import ABCMeta, abstractmethod
import os

from library.mysql_models import *
import library.XmlParsers as XmlParsers


class BaseWriter(metaclass=ABCMeta):
    """Parse XML files and write to database"""
    def __init__(self, source_file):
        self.source_file = source_file

    @abstractmethod
    def process(self):
        pass


class InningWriter(BaseWriter):
    def process(self):
        for table, vals in XmlParsers.InningParser(self.source_file).process():
            if table == 'atbat':
                engine.execute(atbat.insert(vals))
            elif table == 'pitch':
                engine.execute(pitch.insert(vals))
            elif table == 'runner':
                engine.execute(runner.insert(vals))
            else:
                pass


class RawBoxscoreWriter(BaseWriter):
    def process(self):
        for table, vals in XmlParsers.RawBoxscoreParser(self.source_file).process():
            if table == 'batter':
                engine.execute(batter.insert(vals))
            elif table == 'boxscore':
                engine.execute(boxscore.insert(vals))
            elif table == 'linescore':
                engine.execute(linescore.insert(vals))
            elif table == 'pitcher':
                engine.execute(pitcher.insert(vals))
            elif table == 'team':
                engine.execute(team.insert(vals))
            elif table == 'umpire':
                engine.execute(umpire.insert(vals))
            else:
                pass


class LinescoreWriter(BaseWriter):
    def process(self):
        for table, vals in XmlParsers.LinescoreParser(self.source_file).process():
            if table == 'game':
                engine.execute(game.insert(vals))
            elif table == 'inningscore':
                engine.execute(inningscore.insert(vals))
            else:
                pass


class PlayerWriter(BaseWriter):
    def process(self):
        for table, vals in XmlParsers.PlayerParser(self.source_file).process():
            if table == 'player':
                engine.execute(player.insert(vals))
            elif table == 'coach':
                engine.execute(coach.insert(vals))
            else:
                pass
