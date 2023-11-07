"""Functions for reading and writing in files"""
import json
import logging
import os
from typing import Dict


def write_to_dict(file_name: str, key_to_write: str, value_to_write: str) -> None:
    """
    Writes pair key-value in the given dictionary
    If there is no such file, creates it
    Raises KeyError if a given key already is in the dictionary keys
    :param file_name: name of the dictionary
    :param key_to_write: key for the pair
    :param value_to_write: value for the pair
    :return: None
    """
    target_dict = dict()  # If dictionary doesn't exist yet

    try:
        target_dict = read_dict(file_name)  # To read from existing
    except FileNotFoundError:
        logging.info(f'Dictionary {file_name} will be created')
        pass

    keys = target_dict.keys()
    if key_to_write not in keys:
        target_dict[key_to_write] = value_to_write
        with open(file_name, 'w') as file:
            json.dump(target_dict, file)
            logging.debug(f'File {file_name} was saved')
    else:
        logging.error(f'Key {key_to_write} already exists in dictionary {file_name}')
        raise KeyError('Такой ключ существует в словаре')


def read_dict(file_name: str) -> Dict:
    """
    Reads data from json file in a dictionary
    If file does not exist, raises FileNotFoundError
    :param file_name: file for reading
    :return: dictionary with file content
    """
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            content = json.load(file)
            logging.debug(f'File {file_name} was read')
            return content
    else:
        logging.error(f'File {file_name} not found')
        raise FileNotFoundError('Указанный файл не найден')
