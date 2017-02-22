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
            else:
                pass

class PlayersParser(BaseParser):
    player_attribs = {
        'id',
        'first',
        'last',
        'num',
        'rl',
        'bats',
        'position',
        'status',
        'team_abbrev',
        'team_id'
    }

    umpire_attrib = {
        'position',
        'id',
        'first',
        'last'
    }

    coach_attrib = {
       'position',
       'first',
       'last',
       'id'
    }

    def process(self):
        xml_text = read_file(self.file_loc)
        xml_parsed = etree.fromstring(xml_text)

        for elem in xml_parsed.iter():
            if elem.tag == 'team':
                team_type = elem.attrib['type']
            elif elem.tag == 'player':
                player = {
                    'gid': self.gid,
                    'team_type': self.team_type,
                    **{k: v for k, v in elem.attrib.items() if k in self.player_attribs}
                }
                yield 'player', player
            elif elem.tag == 'umpire':
                umpire = {
                    'gid': self.gid,
                    **{k: v for k, v in elem.attrib.items() if k in self.umpire_attribs}
                }
                yield 'umpire', umpire
            elif elem.tag == 'coach':
                coach = {
                    'gid': self.gid,
                    'team_type': self.team_type,
                    **{k: v for k, v in elem.attrib.items() if k in self.coach_attribs}
                }
                yield 'coach', coach
            else:
                pass

class LinescoreParser(BaseParser):
    game_attribs = {
        'venue',
        'game_pk',
        'time',
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
        'game_type',
        'tiebreaker_sw',
        'venue_id',
        'away_name_abbrev',
        'home_name_abbrev',
        'away_code',
        'away_file_code',
        'away_team_id',
        'away_team_city',
        'away_team_name',
        'away_division',
        'away_league_id',
        'away_sport_code',
        'home_code',
        'home_file_code',
        'home_team_id',
        'home_team_city',
        'home_team_name',
        'home_division',
        'home_league_id',
        'home_sport_code',
        'day',
        'double_header_sw',
        'game_nbr',
        'away_games_back',
        'home_games_back',
        'away_games_back_wildcard',
        'home_games_back_wildcard',
        'venue_w_chan_loc',
        'location',
        'away_win',
        'away_loss',
        'home_win',
        'home_loss',
        'league',
        'status',
        'away_team_runs',
        'home_team_runs',
        'away_team_hits',
        'home_team_hits',
        'away_team_errors',
        'home_team_errors',
        'tv_station'
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
            else:
                pass

if __name__ == '__main__':
    list(InningParser('/Users/bruce/Projects/mlbam_scraper/data/mlbam_2016/inning_all/gid_2016_04_03_nynmlb_kcamlb_1.xml').process())
