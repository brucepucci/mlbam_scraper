from bs4 import BeautifulSoup
import requests

VALID_YEARS = {str(year) for year in range(2016, 2017)}
VALID_MONTHS = {str(month).zfill(2) for month in range(3, 11)}
VALID_DAYS = {str(day).zfill(2) for day in range(1, 32)}


class GidScraper:
    """Obatain regular season, completed game ids from mlbam_test"""
    year = slice(5, 9)
    month = slice(6, 8)
    day = slice(4, 6)

    def __init__(self, years=VALID_YEARS,
                 months=VALID_MONTHS, days=VALID_DAYS):
        self.years = years
        self.months = months
        self.days = days

    @classmethod
    def get_page_text(cls, url):
        page = requests.get(url)
        if page.status_code == 200:
            return page.text
        else:
            print(f'Non 200 status on {url}')

    @classmethod
    def get_soup(cls, url):
        page = cls.get_page_text(url)
        return BeautifulSoup(page, 'html.parser')

    @classmethod
    def is_official_regular_season_game(cls, url):
        try:
            soup = cls.get_soup(url + 'linescore.xml')
            reg_season = soup.game.get('game_type') == 'R'
            completed = soup.game.get('status') in ['Final', 'Completed Early']
            return reg_season and completed
        except:
            return False

    def get_gids(self, base_url='http://gd2.mlb.com/components/game/mlb/'):
        """Recursive calls to traverse file system for valid games"""
        soup = self.get_soup(base_url)

        for link in soup.find_all('a'):
            dest = link.get('href')
            if dest.startswith('year_') and dest[self.year] in self.years:
                yield from self.get_gids(base_url + dest)
            elif dest.startswith('month_') and dest[self.month] in self.months:
                yield from self.get_gids(base_url + dest)
            elif dest.startswith('day_') and dest[self.day] in self.days:
                yield from self.get_gids(base_url + dest)
            elif dest.startswith('gid_'):
                if self.is_official_regular_season_game(base_url + dest):
                    yield base_url + dest
            else:
                pass
