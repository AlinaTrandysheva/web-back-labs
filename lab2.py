from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab2 = Blueprint('lab2', __name__, url_prefix='/lab2')

@lab2.route('/lab2/a/')
def a():
    return 'ok'

flower_list = [
    {'name': 'роза',      'price': 300},
    {'name': 'тюльпан',   'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка',   'price': 330},
]

@lab2.route('/flowers')
def list_flowers():
    return render_template('lab2/flower_list.html', flower_list=flower_list) 

@lab2.route('/flowers/<int:flower_id>')
def flowers(flower_id):
    if not (0 <= flower_id < len(flower_list)):
        abort(404)
    f = flower_list[flower_id]
    return render_template('lab2/flower_detail.html',
                           flower_id=flower_id, name=f['name'], price=f['price'])

@lab2.route('/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    del flower_list[flower_id]
    return redirect(url_for('lab2.list_flowers'))


@lab2.route('/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.list_flowers'))

@lab2.route('/add_flower/<name>')
def add_flower(name):
    default_price = 300 + (len(flower_list) % 10) * 10
    flower_list.append({'name': name, 'price': default_price})
    return redirect(url_for('lab2.list_flowers'))

@lab2.route('/add_flower/')
def add_flower_missing():
    return render_template('lab2/flower_missing_400.html'), 400


@lab2.route('/example')
def example():
    name, lab_num, group, course = 'Алина Трандышева', 2, 'ФБИ-34', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)

@lab2.route('/examplebez')
def examplebez():
    return render_template('lab2/example.html')


@lab2.route('/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
<!doctype html>
<html>
  <body>
    <h1>Расчёт с параметрами:</h1>
    <ul>
      <li>{a} + {b} = {a + b}</li>
      <li>{a} - {b} = {a - b}</li>
      <li>{a} * {b} = {a * b}</li>
      <li>{a} / {b} = {'деление на 0' if b == 0 else a / b}</li>
      <li>{a}<sup>{b}</sup> = {a ** b}</li>
    </ul>
  </body>
</html>
'''


@lab2.route('/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1)) 


@lab2.route('/calc/<int:a>')
def calc_one_arg(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


books = [
    {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман", "pages": 2000},
    {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Роман", "pages": 700},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Роман", "pages": 400},
    {"title": "Анна Каренина", "author": "Лев Толстой", "genre": "Роман", "pages": 800},
    {"title": "Отцы и дети", "author": "Иван Тургенев", "genre": "Роман", "pages": 300},
    {"title": "Обломов", "author": "Иван Гончаров", "genre": "Роман", "pages": 540},
    {"title": "Тихий Дон", "author": "Михаил Шолохов", "genre": "Роман", "pages": 1000},
    {"title": "Чевенгур", "author": "Андрей Платонов", "genre": "Роман", "pages": 560},
    {"title": "Двенадцать", "author": "Александр Блок", "genre": "Поэма", "pages": 203},
    {"title": "Доктор Живаго", "author": "Борис Пастернак", "genre": "Роман", "pages": 867}
]

@lab2.route('/books')
def show_books():
    return render_template('lab2/books.html', books=books)


berries = [
    {"name": "Клубника", "desc": "Сладкая садовая ягода.", "img": "berries/klubnika.jpg"},
    {"name": "Земляника", "desc": "Ароматная лесная родственница клубники.", "img": "berries/zemlyanika.jpg"},
    {"name": "Малина", "desc": "Мягкая, нежная, богата витамином C.", "img": "berries/malina.webp"},
    {"name": "Ежевика", "desc": "Сочная тёмная ягода с ноткой кислинки.", "img": "berries/ежевика.webp"},
    {"name": "Голубика", "desc": "Крупная синяя ягода, близка к чернике.", "img": "berries/голубика.webp"},
    {"name": "Черника", "desc": "Лесная ягода, полезна для зрения.", "img": "berries/черника.jpg"},
    {"name": "Клюква", "desc": "Кислая болотная ягода, хороша к мясу.", "img": "berries/клюква.jpg"},
    {"name": "Брусника", "desc": "Кисло-сладкая, хранится долго.", "img": "berries/брусника.webp"},
    {"name": "Облепиха", "desc": "Ярко-оранжевая, очень маслянистая.", "img": "berries/облепиха.webp"},
    {"name": "Шиповник", "desc": "Плод розы, лидер по витамину C.", "img": "berries/шиповник.jpg"},
    {"name": "Крыжовник", "desc": "Зелёный/красный, освежающая кислинка.", "img": "berries/крыжовник.jpg"},
    {"name": "Красная смородина", "desc": "Прозрачные кисти, яркая кислинка.", "img": "berries/смородина.webp"},
    {"name": "Чёрная смородина", "desc": "Сильный аромат листа и ягоды.", "img": "berries/черная смородина.jpg"},
    {"name": "Вишня", "desc": "Кисло-сладкие ароматные ягоды.", "img": "berries/вишня.webp"},
    {"name": "Жимолость", "desc": "Ранняя синяя ягода вытянутой формы.", "img": "berries/жимолость.webp"},
    {"name": "Черешня", "desc": "Сладкие плотные ягоды.", "img": "berries/черешня.webp"},
    {"name": "Барбарис", "desc": "Кислые продолговатые ягодки.", "img": "berries/барбарис.webp"},
    {"name": "Черёмуха", "desc": "Терпкая костянка для выпечки.", "img": "berries/черемуха.webp"},
    {"name": "Морошка", "desc": "Северная янтарная, редкая и ценная.", "img": "berries/морошка.webp"},
    {"name": "Рябина", "desc": "Горьковатая, после морозца слаще.", "img": "berries/рябина.webp"},
    {"name": "Калина", "desc": "Ярко-красная, лечебная горчинка.", "img": "berries/калина.webp"},
    {"name": "Арбуз", "desc": "Сладкая сочная летняя ягода", "img": "berries/арбуз.webp"},
]

@lab2.route('/berries')
def show_berries():
    return render_template('lab2/berries.html', items=berries)


from flask import send_from_directory

