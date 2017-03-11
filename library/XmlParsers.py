from abc import ABCMeta, abstractmethod
from xml.etree import cElementTree as etree

from library.MySqlModels import *

def read_file(file_loc):
    with open(file_loc, 'rt') as f:
        text = f.read()
    return text


class BaseParser(metaclass=ABCMeta):
    """Read/Parse XML, transform into table stuctures specified in mysql_models"""
    def __init__(self, file_loc):
        self.file_loc = file_loc
        self.gid = next(x for x in file_loc.split('/') if
                        x.startswith('gid')).split('.', 1)[0]

    @abstractmethod
    def process(self):
        pass


class InningParser(BaseParser):
    atbat_attribs = set(atbat.columns.keys()) - {'gid', 'inn', 'inn_half', 'b_team', 'p_team'}
    runner_attribs = set(runner.columns.keys()) - {'gid', 'atbat_id'}
    pitch_attribs = set(pitch.columns.keys()) - {'gid', 'atbat_id'}

    def process(self):
        xml_text = read_file(self.file_loc)
        xml_parsed = etree.fromstring(xml_text)

        for elem in xml_parsed.iter():
            if elem.tag == 'inning':
                inning_number = elem.attrib['num']
                home_team = elem.attrib['home_team']
                away_team = elem.attrib['away_team']
            elif elem.tag in ['top', 'bottom']:
                inning_position = elem.tag
                if elem.tag == 'top':
                    batting_team = away_team
                    fielding_team = home_team
                else:
                    batting_team = home_team
                    fielding_team = away_team
            elif elem.tag == 'atbat':
                atbat_id = elem.attrib['num']
                atbat = {
                    'gid': self.gid,
                    'inn': inning_number,
                    'inn_half': inning_position,
                    'b_team': batting_team,
                    'p_team': fielding_team,
                    **{k: v for k, v in elem.attrib.items() if k in self.atbat_attribs}
                }
                atbat.update({elem: None for elem in self.atbat_attribs - atbat.keys()})
                yield 'atbat', atbat
            elif elem.tag == 'pitch':
                pitch = {
                    'gid': self.gid,
                    'atbat_id': atbat_id,
                    **{k: v for k, v in elem.attrib.items() if k in self.pitch_attribs}
                }
                pitch.update({elem: None for elem in self.pitch_attribs - pitch.keys()})
                yield 'pitch', pitch
            elif elem.tag == 'runner':
                runner = {
                    'gid': self.gid,
                    'atbat_id': atbat_id,
                    **{k: v for k, v in elem.attrib.items() if k in self.runner_attribs}
                }
                runner.update({elem: None for elem in self.runner_attribs - runner.keys()})
                yield 'runner', runner
            else:
                pass


class RawBoxscoreParser(BaseParser):
    boxscore_attribs = set(boxscore.columns.keys()) - {'gid'}
    umpire_attribs = set(umpire.columns.keys()) - {'gid'}
    linescore_attribs = set(linescore.columns.keys()) - {'gid'}
    team_attribs = set(team.columns.keys()) - {'gid'}
    pitcher_attribs = set(pitcher.columns.keys()) - {'gid', 'team_code'}
    batter_attribs = set(batter.columns.keys()) - {'gid', 'team_code'}

    def process(self):
        xml_text = read_file(self.file_loc)
        xml_parsed = etree.fromstring(xml_text)

        for elem in xml_parsed.iter():
            if elem.tag == 'boxscore':
                boxscore = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.boxscore_attribs}
                }
                boxscore.update({elem: None for elem in
                                 self.boxscore_attribs - boxscore.keys()})
                yield 'boxscore', boxscore
            elif elem.tag == 'linescore':
                linescore = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.linescore_attribs}
                }
                linescore.update({elem: None for elem in
                                  self.linescore_attribs - linescore.keys()})
                yield 'linescore', linescore
            elif elem.tag == 'umpire':
                umpire = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.umpire_attribs}
                }
                umpire.update({elem: None for elem in
                               self.umpire_attribs - umpire.keys()})
                yield 'umpire', umpire
            elif elem.tag == 'team':
                team_code = elem.attrib['team_code']
                team = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.team_attribs}
                }
                team.update({elem: None for elem in
                             self.team_attribs - team.keys()})
                yield 'team', team
            elif elem.tag == 'pitcher':
                pitcher = {
                    'gid': self.gid,
                    'team_code': team_code,
                    **{k: v for k, v in elem.attrib.items() if k in self.pitcher_attribs}
                }
                pitcher.update({elem: None for elem in
                             self.pitcher_attribs - pitcher.keys()})
                yield 'pitcher', pitcher
            elif elem.tag == 'batter':
                batter = {
                    'team_code': team_code,
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.batter_attribs}
                }
                batter.update({elem: None for elem in
                             self.batter_attribs - batter.keys()})
                yield 'batter', batter
            else:
                pass


class LinescoreParser(BaseParser):
    inningscore_attribs = set(inningscore.columns.keys()) - {'gid'}
    game_attribs = set(game.columns.keys()) - {'gid'}

    def process(self):
        xml_text = read_file(self.file_loc)
        xml_parsed = etree.fromstring(xml_text)

        for elem in xml_parsed.iter():
            if elem.tag == 'game':
                game = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.game_attribs}
                }
                game.update({elem: None for elem in self.game_attribs - game.keys()})
                yield 'game', game
            elif elem.tag == 'linescore':
                inningscore = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.inningscore_attribs}
                }
                inningscore.update({elem: None for elem in self.inningscore_attribs - inningscore.keys()})
                yield 'inningscore', inningscore
            else:
                pass


class PlayerParser(BaseParser):
    player_attribs = set(player.columns.keys()) - {'gid'}
    coach_attribs = set(coach.columns.keys()) - {'gid'}

    def process(self):
        xml_text = read_file(self.file_loc)
        xml_parsed = etree.fromstring(xml_text)

        for elem in xml_parsed.iter():
            if elem.tag == 'coach':
                coach = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.coach_attribs}
                }
                coach.update({elem: None for elem in self.coach_attribs - coach.keys()})
                yield 'coach', coach
            elif elem.tag == 'player':
                player = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.player_attribs}
                }
                player.update({elem: None for elem in self.player_attribs - player.keys()})
                yield 'player', player
            else:
                pass
