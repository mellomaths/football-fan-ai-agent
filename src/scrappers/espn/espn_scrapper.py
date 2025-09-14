from scrappers.espn.espn_scrapper_api import EspnScrapperApi
from scrappers.espn.espn_scrapper_html import EspnScrapperHTML


class EspnScrapper:

    def __init__(self):
        self.api_scrapper = EspnScrapperApi()
        self.html_scrapper = EspnScrapperHTML()

    def get_upcoming_matches(self, team: str):
        team = team.upper()
        data = self.html_scrapper.get_data(team)
        return self.html_scrapper.parse_matches(data)
