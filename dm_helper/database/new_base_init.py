import os
from typing import Annotated
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped

app = Flask(__name__)

path = os.getcwd() + '/test.db'
engine = create_engine('sqlite:///' + path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path
db = SQLAlchemy(app)

fractions = db.Table('fractions', db.metadata,
                     db.Column('char_id', db.ForeignKey('character.id')),
                     db.Column('group_id', db.ForeignKey('group.id')))

intpk = Annotated[int, mapped_column(primary_key=True)]
unique_name = Annotated[str, mapped_column(unique=True)]


class Race(db.Model):
    __tablename__ = "race"
    id: Mapped[intpk]
    name: Mapped[unique_name]

    def __repr__(self):
        return '<Race %r>' % self.name


class Group(db.Model):
    __tablename__ = "group"
    id: Mapped[intpk]
    name: Mapped[unique_name]
    participants: Mapped[list["Character"]] = db.relationship(viewonly=True, secondary=fractions,
                                                              back_populates='groups')

    def __repr__(self):
        return '<Group %r>' % self.name


class Character(db.Model):
    __tablename__ = "character"
    id: Mapped[intpk]
    name: Mapped[str]
    race_id: Mapped[int] = mapped_column(db.ForeignKey('race.id'))
    groups: Mapped[list["Group"]] = db.relationship(secondary=fractions, back_populates='participants')
    money: Mapped[int] = mapped_column(default=0)
    currency: Mapped[int] = mapped_column(default=0)
    items: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    race: Mapped[Race] = db.relationship("Race")

    # __table_args__ = (
    #     CheckConstraint(money >= 0, name='check_money_positive'),
    #     CheckConstraint(currency >= 0, name='check_currency_positive'),
    # )

    def __repr__(self):
        return '<Character %r>' % self.name


@app.route('/')
def home():
    with app.app_context():
        db.drop_all()
        db.create_all()
    # add_chars()
    return '<h1> Base created! </h1>'


def add_chars():
    race_1 = Race(name='Cat')
    race_2 = Race(name='Human')
    race_3 = Race(name='Mekklar')
    db.session.add_all([race_1, race_2, race_3])
    db.session.commit()

    group_1 = Group(name='Mrrshan')
    group_2 = Group(name='Niau')
    group_3 = Group(name='Mages')
    group_4 = Group(name='Fighters')
    group_5 = Group(name='Pirates')
    db.session.add_all([group_1, group_2, group_3, group_4, group_5])

    char_1 = Character(name='Kate', race=race_1, money=20, items='items_1', description='long tail')
    char_2 = Character(name='Mike', race=race_2, money=500, items='items_2', description='tall man')
    char_3 = Character(name='Shir', race=race_1, money=12, currency=15, items='items_3',
                       description='white furry cat')
    char_1.groups.append(group_2)
    char_1.groups.append(group_5)
    char_2.groups.append(group_3)
    char_2.groups.append(group_5)
    char_3.groups.append(group_4)

    db.session.add_all([char_1, char_2, char_3])
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
