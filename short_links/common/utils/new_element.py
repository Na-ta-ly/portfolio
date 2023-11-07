"""Functions for adding new element procedure"""
import logging
import os
import random
from typing import Dict

from common.settings import storage_path
from common.utils.file_functions import write_to_dict
from common.utils.regex import get_pseudo, get_home_link, reduce_pseudo


def add_pseudo(base: Dict, link: str) -> str:
    """
    Adds pseudo for a new link
    If pseudo presents in base, returns pseudo anyway
    :param base: base, containing other pseudos in '_pseudo' section
    :param link: URL for processing
    :return: pseudo, corresponding to the link
    """
    pseudo = get_pseudo(link)
    logging.debug(f'For {link} got pseudo {pseudo}')

    if base.get('_pseudo', None) is None:
        base['_pseudo'] = dict()
        logging.info(f'Created section _pseudo in base')

    if pseudo not in base['_pseudo'].keys():
        pseudos_dict_file_name = storage_path + os.sep + '_home_pages.json'
        home_address = get_home_link(link)
        write_to_dict(pseudos_dict_file_name, pseudo, home_address)
        base['_pseudo'][pseudo] = home_address
        logging.info(f'Pseudo {pseudo} was added to base')

    return pseudo


def add_to_index(base: Dict, reduced_pseudo: str, pseudo: str) -> None:
    """
    Adds pair reduced_pseudo - pseudo to the _index.json
    :param base: base for work
    :param reduced_pseudo: short pseudo
    :param pseudo: full pseudo
    :return: None
    """
    if reduced_pseudo not in base.keys():
        main_dict_file_name = storage_path + os.sep + '_index.json'
        write_to_dict(main_dict_file_name, reduced_pseudo, pseudo)
        logging.debug(f'Short pseudo {reduced_pseudo} was got for {pseudo}')


def add_new_dictionary(base: Dict, pseudo: str, short_name: str) -> str:
    """
    Creates a new file with dictionary for a new pseudo
    Init dictionary with pseudo to link short pseudo with full one
    If dictionary exists, returns its file_name
    :param base: base for work
    :param pseudo: full pseudo
    :param short_name: reduced pseudo
    :return: file_name of a dictionary
    """
    file_name = storage_path + os.sep + pseudo + '.json'
    if not os.path.isfile(file_name):
        logging.info(f'Dictionary {pseudo} will be created')
        write_to_dict(file_name, '_pseudo', pseudo)
        base[short_name] = dict()
        base[short_name]['_pseudo'] = pseudo
    return file_name


def add_short_address(base: Dict, section: str, link: str, file_name: str) -> str:
    """
    Adds new link in a given section of the base
    If link is already in base, returns its short_address
    Saving info in file
    :param base: base for work
    :param section: name of section for adding new link
    :param link: value, that will be added
    :param file_name: name of corresponding file
    :return: short_address for the link
    """
    if link not in base[section].values():
        check = ''
        while check is not None:
            suffix = generate_suffix(4, 97, 122)
            short_address = section + '/' + suffix
            check = base[section].get(short_address, None)
        write_to_dict(file_name, short_address, link)
        logging.debug(f'Pair {short_address} - {link} written to {file_name}')
        base[section][short_address] = link
    else:
        short_address = get_key_by_value(base[section], link)
        logging.info('Link is already in base')
    return short_address


def generate_suffix(length: int, limit_lo: int, limit_hi: int) -> str:
    """
    Generates suffix for a short link
    :param length: number characters in the suffix
    :param limit_lo: low number of a char (ASCII)
    :param limit_hi: high number of a char (ASCII)
    :return: string of random chars of chosen length
    """
    suffix = ''
    for _ in range(length):
        suffix += chr(random.randint(limit_lo, limit_hi))
    return suffix


def get_reduced_pseudo(base: Dict, length: int, pseudo: str) -> str:
    """
    Creates a new reduced pseudo
    If there is already given pseudo in the base, returns existing short pseudo
    :param base: dictionary-based base for check
    :param length: number characters in the reduced pseudo
    :param pseudo: processing pseudo
    :return: short pseudo
    """
    inner_pseudo = pseudo
    if len(pseudo) < length - 1:  # To avoid short reduced pseudos
        inner_pseudo = pseudo + 'a' * length
    short_pseudo = initial_short_pseudo = reduce_pseudo(inner_pseudo, length)
    check = base.get(initial_short_pseudo, None)

    if check is not None and check.get('_pseudo', None) != pseudo:
        short_pseudos = iter(base.keys())  # Seek among existing
        try:
            while base[short_pseudo].get('_pseudo', None) != pseudo:
                short_pseudo = next(short_pseudos)
        except StopIteration:
            pass

        check = base.get(short_pseudo, None)
        while check is not None and check.get('_pseudo', None) != pseudo:  # Generate new till unique
            short_pseudo = initial_short_pseudo[:4] + generate_suffix(2, 97, 122)
            check = base.get(short_pseudo, None)

    return short_pseudo


def get_key_by_value(base: Dict, value: str) -> str:
    """
    Seeks value in the dictionary and returns corresponding key
    If there is no such value in the dictionary, returns None
    If there are several equal values, returns the last one
    :param base: dictionary for search
    :param value: target value
    :return: key, corresponding to given value
    """
    target_key = None
    for dict_key, dict_value in base.items():
        if dict_value == value:
            target_key = dict_key
    return target_key
