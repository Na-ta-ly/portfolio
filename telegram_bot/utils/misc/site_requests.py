from datetime import date
from typing import List
from utils.misc.get_response import get_response
from config_data.classes import SiteSettings
from utils.misc.results_postprocessing import get_pilots_list
from config_data import globals


class SiteApiInterface:

    def __init__(self) -> None:
        self._headers = {
            'x-rapidapi-key': SiteSettings().api_key.get_secret_value(),
            'x-rapidapi-host': SiteSettings().api_host
        }
        self._timeout = 200

        if globals.seasons is None:  # Request once a session
            globals.seasons = self._get_years()
        self.seasons = globals.seasons

    def get_pilots(self, year: int = date.today().year, reverse: bool = False) -> str:
        """Returns sorted list of pilots as str
        reverse: True - reversed order, False - right order"""
        url = "https://" + self._headers['x-rapidapi-host'] + "/rankings/drivers"
        if year not in self.seasons:
            return 'Информация об указанном сезоне отсутствует на сайте'
        response = get_response("GET", url, self._headers, {"season": str(year)},
                                self._timeout)
        return get_pilots_list(response, reverse=reverse)

    def _get_years(self) -> List[int]:
        """Returns list of available seasons as int"""
        url = "https://" + self._headers['x-rapidapi-host'] + "/seasons"
        response = get_response("GET", url, self._headers, {},
                                self._timeout)
        return response.get('response', [])
