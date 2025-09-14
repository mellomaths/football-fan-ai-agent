class EspnConfig:

    def __init__(self):
        self.url = {
            "FLAMENGO": {
                "site": "https://www.espn.com/soccer/team/fixtures/_/id/819/flamengo",
                "api": "https://site.api.espn.com/apis/site/v2/sports/soccer/bra.1/teams/819/schedule",
            },
        }

    def get_website_url(self, team: str):
        return self.url.get(team, {}).get("site")

    def get_api_url(self, team: str):
        return self.url.get(team, {}).get("api")
