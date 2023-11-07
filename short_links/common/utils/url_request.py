"""Function, working with requests"""
import logging
import requests


def get_status(link: str) -> int:
    """
    Gets response for the link
    :param link: link for check
    :return: status_code for the link
    """
    response = requests.request('GET', link)
    logging.info(f'Request sent to {link}')
    return response.status_code
