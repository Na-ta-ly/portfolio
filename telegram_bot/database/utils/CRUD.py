from peewee import OperationalError
from database.common.models import db, History


class CRUDInterface:
    @classmethod
    def create(cls, user_name: str, request: str) -> None:
        """Adds new row to the database"""
        try:
            with db.atomic():
                History.create(user=user_name, request=request)
        except OperationalError:  # If base isn't created yet
            db.create_tables([History])
            db.close()
            CRUDInterface.create(user_name, request)

    @classmethod
    def retrieve(cls, user_name: str, number: int) -> str:
        """Returns number of last requests from user_name"""
        try:
            with db.atomic():
                query = (History
                         .select()
                         .where(History.user == user_name))
            return '\n'.join([' - '.join([item.created_date.strftime('%d/%m/%y %H:%M'),
                                          item.user, item.request])
                              for item_number, item in enumerate(query[::-1])
                              if item_number < number])
        except OperationalError:  # If base isn't created yet
            db.create_tables([History])
            db.close()
            CRUDInterface.retrieve(user_name, number)
