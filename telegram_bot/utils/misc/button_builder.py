from typing import List
from telegram import InlineKeyboardButton
from utils.misc.site_requests import SiteApiInterface


def get_year_buttons() -> List:
    """Returns list of buttons with available years"""
    option_list = []
    seasons = SiteApiInterface().seasons
    string = []
    for year in seasons:
        string.append(InlineKeyboardButton(str(year), callback_data=year))
        if len(string) >= 5:
            option_list.append(string)
            string = []
    else:
        option_list.append(string)
    return option_list
