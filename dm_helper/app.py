import operator
import os
from flask import Flask, render_template, request, \
    redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from database.new_base_init import Character, Race, Group

app = Flask(__name__)

path = os.getcwd() + '/database/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path
app.config['SECRET_KEY'] = 'j32u4g23j4123l4'
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def home():
    characters = db.session.query(Character).order_by(Character.id).all()
    return render_template('home.html', items=characters)


@app.route('/<int:char_id>', methods=['GET', 'POST'])
def one_character(char_id):
    character = db.session.query(Character).get_or_404(char_id)
    groups = character.groups
    if request.method == 'POST':
        new_char = get_char_data(request)
        copy_char(character, new_char)
        if request.args.get('opt') == 'sub':
            func = operator.sub
        else:
            func = operator.add
        account = request.args.get('account')
        if account == 'money':
            number = int(request.form.get('money_delta', 0))
            character.money = func(character.money, number)
        else:
            number = int(request.form.get('currency_delta', 0))
            character.currency = func(character.currency, number)
        try:
            db.session.commit()
            flash("Персонаж успешно обновлен", 'info')
        except:
            flash("Не удалось обновить данные персонажа", 'error')
    return render_template('show_char.html', char=character,
                           groups=groups)


@app.route('/add', methods=['GET', 'POST'])
def new_character():
    races = [item for item in db.session.query(Race).all()]
    if request.method == 'POST':
        char = get_char_data(request)
        option = request.args.get('opt')
        try:
            db.session.add(char)
            db.session.commit()
            char = db.session.query(Character).filter(Character.name == char.name and
                                                      Character.race == char.race).first()
            flash("Создан новый персонаж", category='info')
        except:
            flash("Не удалось создать персонажа", category='error')
        if option == 'groups':
            return redirect('/groups/' + str(char.id))
        else:
            return redirect('/' + str(char.id))
    else:
        empty_character = Character(name='Новый персонаж', race=db.session.query(Race).first())
        return render_template('new_char.html', char=empty_character, races=races)


@app.route('/update/<int:char_id>', methods=['GET', 'POST'])
def edit_character(char_id):
    if request.method == 'POST':
        char = db.session.query(Character).get_or_404(char_id)
        new_char = get_char_data(request)
        copy_char(char, new_char)
        try:
            db.session.commit()
        except:
            flash("Не удалось обновить данные персонажа", 'error')
        return redirect('/' + str(char_id))
    else:
        character = db.session.query(Character).get_or_404(char_id)
        races = [item for item in db.session.query(Race).all()]
        groups = [item for item in db.session.query(Group).all()]
        groups = filter(lambda item: item not in character.groups, groups)
        return render_template('update_char.html', char=character, races=races,
                               groups=groups)


@app.route('/delete/<int:char_id>', methods=["POST"])
def delete_character(char_id):
    char_to_del = db.session.query(Character).get_or_404(char_id)
    try:
        db.session.delete(char_to_del)
        db.session.commit()
        flash("Персонаж удален", 'info')
        return redirect('/')
    except:
        flash("Не удалось удалить персонажа", 'error')


@app.route('/groups/<int:char_id>', methods=["POST", "GET"])
def get_groups(char_id):
    if request.method == 'POST':
        char = db.session.query(Character).get_or_404(char_id)
        option = request.args.get('opt')
        if option == 'add':
            group_names = request.form.getlist('all_groups')
            new_group_names = add_new_groups(request)
            new_group_names.extend(group_names)
            for group_name in new_group_names:
                if group_name:
                    group = db.session.query(Group).filter(Group.name == group_name).first()
                    char.groups.append(group)
            try:
                db.session.commit()
                flash("Группы успешно добавлены", 'info')
            except:
                flash("Не удалось обновить данные персонажа", 'error')
            return redirect('/groups/' + str(char_id))
        else:
            group_names = request.form.getlist('groups')
            for group_name in group_names:
                if group_name:
                    group = db.session.query(Group).filter(Group.name == group_name).first()
                    char.groups.remove(group)
            try:
                db.session.commit()
                flash("Группы успешно удалены", 'info')
            except:
                flash("Не удалось обновить данные персонажа", 'error')
            return redirect('/groups/' + str(char_id))
    else:
        character = db.session.query(Character).get_or_404(char_id)
        groups = [item for item in db.session.query(Group).all()]
        groups = filter(lambda item: item not in character.groups, groups)
        return render_template('clan_edit.html', char=character, groups=groups)


@app.errorhandler(404)
def no_page(error):
    return render_template('404_error.html')


@app.errorhandler(IntegrityError)
def integrity_error(error):
    return str(error.orig)


def get_char_data(request):
    char_name = request.form.get('name', None)
    char_race = request.form.get('race', None)
    new_race_name = request.form.get('new_race', None)
    items = request.form.get('items', None)
    money = request.form.get('money', 0)
    currency = request.form.get('currency', 0)
    char_descr = request.form.get('description', None)
    char = Character(name=char_name)
    if new_race_name:
        new_race = Race(name=new_race_name)
        char.race = new_race
        try:
            db.session.add(new_race)
            db.session.commit()
            flash("Новая раса добавлена", 'info')
        except:
            flash("Не удалось добавить новую расу", 'error')
    elif char_race:
        char.race = db.session.query(Race).filter(Race.name == char_race).first()
    if items:
        char.items = items
    if money:
        char.money = int(money)
    if currency:
        char.currency = int(currency)
    if char_descr:
        char.description = char_descr
    return char


def add_new_groups(request):
    result_groups = []
    new_group_names = [request.form.get('new_group_1', None),
                       request.form.get('new_group_2', None),
                       request.form.get('new_group_3', None)]
    for group_name in new_group_names:
        if group_name:
            new_group = Group(name=group_name)
            result_groups.append(new_group.name)
            try:
                db.session.add(new_group)
                db.session.commit()
                flash("Добавлены новые группы", 'info')
            except:
                flash("Не удалось добавить группы", 'error')
    return result_groups


def copy_char(old_char, new_char):
    old_char.name = new_char.name
    old_char.race = new_char.race
    old_char.items = new_char.items
    old_char.money = new_char.money
    old_char.currency = new_char.currency
    old_char.description = new_char.description


if __name__ == '__main__':
    app.run(debug=True)
