from logger.config import logging
from common.messages import show_menu
from common.settings import menu
from common.messages import show_by_pseudo, show_by_short, show_all
from common.messages import show_registration
from common.utils.storage import base_init

if __name__ == '__main__':
    print('Программа для сокращения интернет-адресов')
    try:
        base = base_init()
    except FileNotFoundError:
        base = dict()
        logging.info(f'New base was created')

    while True:
        choice = show_menu()
        if choice == menu['registration']:
            show_registration(base)
        if choice == menu['get_by_pseudo']:
            show_by_pseudo(base)
        if choice == menu['get_by_short']:
            show_by_short(base)
        if choice == menu['get_all']:
            show_all(base)
        if choice == menu['quit']:
            logging.info('Exit program')
            break
