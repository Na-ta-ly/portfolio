from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('my_database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class History(BaseModel):
    created_date = pw.DateTimeField(default=datetime.now)
    user = pw.CharField()
    request = pw.TextField()
