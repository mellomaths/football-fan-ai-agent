class EspnConfig:

    def __init__(self):
        self.tids = {
            "FLAMENGO": 819,
            "PALMEIRAS": 2029,
            "CRUZEIRO": 2022,
            "MIRASSOL": 9169,
            "BAHIA": 9967,
            "BOTAFOGO": 6086,
            "SAO_PAULO": 2026,
            "BRAGANTINO": 6079,
            "CORINTHIANS": 874,
            "FLUMINENSE": 3445,
            "INTERNACIONAL": 1936,
            "CEARA": 9969,
            "GREMIO": 6273,
            "ATLETICO_MG": 7632,
            "VASCO": 3454,
            "SANTOS": 2674,
            "VITORIA": 3457,
            "JUVENTUDE": 6270,
            "FORTALEZA": 6272,
            "SPORT": 7631,
        }

    def get_website_url(self, team: str):
        tid = self.tids.get(team, None)
        if not tid:
            return None
        url = f"https://www.espn.com/soccer/team/fixtures/_/id/{tid}/{team}"
        return url

    def get_api_url(self, team: str):
        tid = self.tids.get(team, None)
        if not tid:
            return None
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/teams/{tid}/schedule"
        return url
