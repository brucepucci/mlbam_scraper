from abc import ABCMeta, abstractmethod
import os

from library.MySqlModels import *
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
        atbats = list()
        pitches = list()
        runners = list()
        for table, vals in XmlParsers.InningParser(self.source_file).process():
            if table == 'atbat':
                atbats.append(vals)
            elif table == 'pitch':
                pitches.append(vals)
            elif table == 'runner':
                runners.append(vals)
            else:
                pass
        engine.execute(atbat.insert(), atbats)
        engine.execute(pitch.insert(), pitches)
        engine.execute(runner.insert(), runners)


class RawBoxscoreWriter(BaseWriter):
    def process(self):
        batters = list()
        pitchers = list()
        umpires = list()

        for table, vals in XmlParsers.RawBoxscoreParser(self.source_file).process():
            if table == 'batter':
                batters.append(vals)
            elif table == 'boxscore':
                engine.execute(boxscore.insert(vals))
            elif table == 'linescore':
                engine.execute(linescore.insert(vals))
            elif table == 'pitcher':
                pitchers.append(vals)
            elif table == 'team':
                engine.execute(team.insert(vals))
            elif table == 'umpire':
                pitchers.append(umpires)
            else:
                pass
        engine.execute(batter.insert(), batters)
        engine.execute(pitcher.insert(), pitchers)
        engine.execute(umpire.insert(), umpires)


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
        players = list()
        coaches = list()
        for table, vals in XmlParsers.PlayerParser(self.source_file).process():
            if table == 'player':
                players.append(vals)
            elif table == 'coach':
                coaches.append(vals)
            else:
                pass
        engine.execute(player.insert(), players)
        engine.execute(coach.insert(), coaches)

