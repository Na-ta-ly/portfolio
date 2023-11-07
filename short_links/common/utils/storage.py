"""Functions organising main actions with base"""
import logging
import os
import re
from typing import List, Dict
from collections.abc import Iterable

from common.utils.file_functions import read_dict
from common.utils.new_element import add_pseudo, add_to_index, add_new_dictionary, add_short_address, get_reduced_pseudo
from common.settings import storage_path


def get_info_by_pseudo(base: Dict, pseudo: str) -> List[str]:
    """
    Gets homepage address for given pseudo
    If there is no pseudo in base, returns [None]
    :param base: dictionary-based base for search
    :param pseudo: pseudo for homepage
    :return: list[homepage_address, pseudo]
    """
    result = base['_pseudo'].get(pseudo, None)
    if result is None:
        info = [None]
    else:
        homepage_address = result
        pseudo = pseudo
        info = [homepage_address, pseudo]
    logging.debug(f'For {pseudo} got {info}')
    return info


def get_info_by_short(base: Dict, short_address: str) -> List[str]:
    """
    Gets full address for given short address
    If there is no short_address in base, returns [None]
    :param base: dictionary-based base for search
    :param short_address: reduced page address
    :return: list[standard_page_address, short_address]
    """
    info = [None]
    result = None

    short_begin = re.split('/', short_address, maxsplit=1)[0]

    for key in base.keys():
        if key == short_begin:
            result = base[key].get(short_address, None)
            break

    if result is not None:
        standard_page_address = result
        short = short_address
        info = [standard_page_address, short]
    logging.debug(f'For {short_address} got {info}')
    return info


def write_new_item(base: Dict, link: str) -> List[str]:
    """
    Generates data for a new link and writes it in the base
    If this link is already in base, returns current values
    Returns [None], if ValueError was occurred
    :param base: dictionary-based base for work
    :param link: standard address for adding to the base
    :return: list[short_address, pseudo, link]
    """
    try:
        pseudo = add_pseudo(base, link)
        reduced_pseudo = get_reduced_pseudo(base, 6, pseudo)
        add_to_index(base, reduced_pseudo, pseudo)

        inner_dict_file_name = add_new_dictionary(base, pseudo, reduced_pseudo)
        short_address = add_short_address(base, reduced_pseudo, link, inner_dict_file_name)
        info = [short_address, pseudo, link]
    except ValueError:
        logging.error(f'Link {link} seems incorrect')
        info = [None]
    return info


def get_all_base(base: Dict) -> Iterable:
    """
    Creates an iterator for printing all base values
    :param base: base for printing
    :return: iterator with list of values (short_link, full_link)
    """
    links_list = ['Псевдонимы:']
    for pseudo, home_page in base['_pseudo'].items():
        links_list.append((pseudo, home_page))

    links_list.append('\nKopоткие интернет-адреса:')
    for short_pseudo, dictionary in base.items():
        if short_pseudo != '_pseudo':
            links_list.append([(key, value) for key, value in dictionary.items() if key != '_pseudo'])
    return links_list.__iter__()


def base_init() -> Dict:
    """
    Reads data from files at the program start
    :return: base dictionary
    """
    base = dict()
    pseudos_dict_file_name = storage_path + os.sep + '_home_pages.json'
    base['_pseudo'] = read_dict(pseudos_dict_file_name)

    short_parts_dict_file_name = storage_path + os.sep + '_index.json'
    short_parts = read_dict(short_parts_dict_file_name)

    for short_start, pseudo in short_parts.items():
        file_name = storage_path + os.sep + pseudo + '.json'
        base[short_start] = read_dict(file_name)

    logging.info(f'Base was successfully read from disk')
    return base
