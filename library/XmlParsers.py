from abc import ABCMeta, abstractmethod
from xml.etree import cElementTree as etree

def read_file(file_loc):
    with open(file_loc, 'rt') as f:
        text = f.read()
    return text


class BaseParser(metaclass=ABCMeta):
    def __init__(self, file_loc):
        self.file_loc = file_loc
        self.gid = next(x for x in file_loc.split('/') if
                        x.startswith('gid')).split('.', 1)[0]

    @abstractmethod
    def process(self):
        pass


class InningParser(BaseParser):
    atbat_attribs = {
        'away_team_runs',
        'b',
        'b_height',
        'batter',
        'des',
        'event',
        'home_team_runs',
        'num',
        'o',
        'p_throws',
        'pitcher',
        's',
        'stand',
        'start_tfs'
    }

    runner_attribs = {
        'end',
        'event',
        'event_num',
        'id',
        'score',
        'start',
    }

    pitch_attribs = {
        'ax',
        'ay',
        'az',
        'break_angle',
        'break_length',
        'break_y',
        'des',
        'end_speed',
        'id',
        'nasty',
        'pfx_x',
        'pfx_z',
        'pitch des',
        'pitch_type',
        'px',
        'pz',
        'spin_dir',
        'spin_rate',
        'start_speed',
        'sz_bot',
        'sz_top',
        'tfs',
        'type',
        'type_confidence',
        'vx0',
        'vy0',
        'vz0',
        'x',
        'x0',
        'y',
        'y0',
        'z0',
        'zone'
    }

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
    boxscore_attribs = {
        'attendance',
        'home_league_id',
        'start_time',
        'venue_id',
        'venue_name',
        'weather',
        'wind'
    }

    umpire_attribs = {
        'id',
        'name',
        'position'
    }

    linescore_attribs = {
        'away_team_errors',
        'away_team_hits',
        'away_team_runs',
        'home_team_errors',
        'home_team_hits',
        'home_team_runs'
    }

    inning_line_score_attribs = {
        'away',
        'home',
        'inning'
    }

    team_attribs = {
        'id',
        'losses',
        'team_code',
        'team_flag',
        'wins'
    }

    pitcher_attribs = {
        'ao',
        'bb',
        'bf',
        'er',
        'game_score',
        'go',
        'h',
        'hr',
        'id',
        'np',
        'out',
        'pitch_order',
        'pos',
        's',
        'so',
        'r'
    }

    batter_attribs = {
        'a',
        'ab',
        'ao',
        'bat_order',
        'bb',
        'cs',
        'd',
        'e',
        'fldg',
        'hbp',
        'hr',
        'id',
        'lob',
        'po',
        'pos',
        'sac',
        'r',
        'rbi',
        'sb',
        'sf',
        'so',
        't',
        'tb'
    }

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
            elif elem.tag == 'inning_line_score':
                inning_line_score = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.inning_line_score_attribs}
                }
                inning_line_score.update({elem: None for elem in
                                          self.inning_line_score_attribs - inning_line_score.keys()})
                yield 'linning_line_score', inning_line_score
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
    inningscore_attribs = {
        'inning',
        'away_inning_runs',
        'home_inning_runs'
    }

    game_attribs = {
        'venue',
        'game_pk',
        'time_date',
        'time_zone',
        'ampm',
        'first_pitch_et',
        'away_time',
        'away_time_zone',
        'away_ampm',
        'home_time',
        'home_time_zone',
        'home_ampm',
        'venue_id',
        'away_name_abbrev',
        'home_name_abbrev',
        'away_code',
        'away_team_id',
        'away_team_city',
        'away_team_name',
        'away_division',
        'away_league_id',
        'home_code',
        'home_team_id',
        'home_team_city',
        'home_team_name',
        'home_division',
        'home_league_id',
        'day',
        'double_header_sw',
        'away_games_back',
        'home_games_back',
        'away_games_back_wildcard',
        'home_games_back_wildcard',
        'venue_w_chan_loc',
        'away_win',
        'away_loss',
        'home_win',
        'home_loss',
        'league',
        'away_team_runs',
        'home_team_runs',
        'away_team_hits',
        'home_team_hits',
        'away_team_errors',
        'home_team_errors'
    }

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
    player_attribs = {
        'id',
        'first',
        'last',
        'num',
        'boxname',
        'rl',
        'bats',
        'position',
        'team_abbv',
        'team_id',
        'bat_order'
    }

    coach_attribs = {
        'id',
        'position',
        'first',
        'last',
        'num'
    }

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
