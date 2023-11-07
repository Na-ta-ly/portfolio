"""Functions, working with regular expressions"""
import re
from typing import List

from common.regex_rules import pseudo_template, pseudo_template_cleaner, \
    home_page_template, valid_address_template


def get_pseudo(link: str) -> str:
    """
    Generates pseudo for a given link by extracting the longest domain name
    If link does not correspond pseudo_template or has empty 1 level domain,
    raises ValueError
    :param link: link for analysis
    :return: pseudo
    """
    test_match = pseudo_template.search(link)
    if test_match is None:
        raise ValueError
    test_match = pseudo_template_cleaner.findall(test_match.group(0))
    if test_match == '':
        raise ValueError
    return get_max_word(test_match)


def get_max_word(words: List) -> str:
    """
    Returns the longest word in the list, or fist of them (if length is equal)
    :param words: list of word for search
    :return: the longest word
    """
    max_element = words[0]
    for word in words:
        if len(word) > len(max_element):
            max_element = word
    return max_element


def get_home_link(link: str) -> str:
    """
    Returns link on the home_page for a given link
    If no match found in the link, raises ValueError
    :param link: URL for analysis
    :return: home_page link
    """
    test_match = home_page_template.search(link)
    if test_match is not None:
        return test_match.group(0)
    else:
        raise ValueError


def reduce_pseudo(pseudo: str, length: int) -> str:
    """
    Inserts '.' in the third position and cuts new value
    :param pseudo: initial full pseudo
    :param length: number of characters that should be in result
    :return: new reduced pseudo
    """
    reduced_pseudo = re.sub(r'(?<=\w{3})', '.', pseudo, count=1)
    return reduced_pseudo[:length]


def check_address(potential_address: str) -> bool:
    """
    Checks if potential_address corresponds the valid_address_template rule
    :param potential_address: URL for check
    :return: True if there is match with the rule
    """
    match = valid_address_template.search(potential_address)
    result = True if match is not None else False
    return result
