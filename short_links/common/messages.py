"""Functions for all menus and dialogs"""
import logging
from typing import List, Dict

from common.settings import menu
from common.utils.storage import get_info_by_pseudo, get_info_by_short, get_all_base
from common.utils.url_request import get_status
from common.utils.storage import write_new_item
from common.utils.regex import check_address


def show_menu() -> str:
    """
    Serves main menu
    :return: user's response
    """
    info_list = [['\nВыберите функцию'],
                 [menu['registration'], '- регистрация короткого интернет-адреса по стандартному'],
                 [menu['get_by_pseudo'], '- получение и проверка домашней страницы интернет-адреса по псевдониму'],
                 [menu['get_by_short'], '- получение и проверка стандартного интернет-адреса по короткому'],
                 [menu['get_all'], '- получение всех пар адресов'],
                 [menu['quit'], '- завершение программы']]
    show_info(info_list)
    return user_request('\nВаш выбор:')


def show_by_pseudo(base: Dict) -> None:
    """
    Shows dialog for homepage address from its pseudo
    :param base: dictionary-based base with data
    :return: None
    """
    pseudo = user_request('Введите псевдоним домашней страницы:')
    logging.info(f'Request by pseudo {pseudo}')
    info = get_info_by_pseudo(base, pseudo)

    if info[0] is None:
        info_list = ['\nАдрес домашней страницы не найден']
    else:
        info_list = [['\nСтандартный интернет-адрес:', info[0]],
                     ['Псевдоним домашней страницы интернет-адреса:', info[1]],
                     ['Код ответа страницы: ', get_status(info[0])]]
    show_info(info_list)


def show_by_short(base: Dict) -> None:
    """
    Shows dialog for full address from reduced one
    :param base: dictionary-based base with data
    :return: None
    """
    short = user_request('Введите сокращенный URL:')
    logging.info(f'Request by short address {short}')
    info = get_info_by_short(base, short)

    if info[0] is None:
        info_list = ['\nСтандартный интернет-адрес не найден']
    else:
        info_list = [['\nСтандартный интернет-адрес:', info[0]],
                     ['Короткий интернет-адрес:', info[1]],
                     ['Код ответа страницы: ', get_status(info[0])]]
    show_info(info_list)


def show_registration(base: Dict) -> None:
    """
    Shows dialog for registration
    :param base: dictionary-based base with data
    :return: None
    """
    standard_address = get_standard_address()
    logging.info(f'Registration for {standard_address}')
    info = write_new_item(base, standard_address)
    if info[0] is None:
        info_list = ['\nВведенные интернет-адрес не корректен']
    else:
        info_list = [['\nКороткий интернет-адрес:', info[0]],
                     ['Псевдоним домашней страницы интернет-адреса:', info[1]],
                     ['Стандартный интернет-адрес:', info[2]]]
    show_info(info_list)


def show_all(base) -> None:
    """
    Shows full base content
    :return: None
    """
    show_info(['\nВсе пары короткий адрес - стандартный адрес:'])
    logging.info('Showing base content')
    for line in get_all_base(base):
        show_info([line])


def show_info(message_list: List[str | List[str]]) -> None:
    """
    Prints list of messages
    :param message_list: separate messages, can be list itself
    :return: None
    """
    for line in message_list:
        if isinstance(line, list):
            print(*line)
        else:
            print(line)


def user_request(message: str) -> str:
    """
    Requests info from user
    :param message: message for user
    :return: lower case response from user
    """
    return input(message + ' ').lower()


def get_standard_address() -> str:
    """
    Requests about standard URL and checks
    If it does not start with 'https://', adds 'https://'
    :return: standard_address
    """
    user_response = user_request('Введите стандартный URL для регистрации:')
    if not check_address(user_response):
        user_response = 'https://' + user_response
    return user_response
