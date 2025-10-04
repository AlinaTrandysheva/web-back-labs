from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
import datetime

app = Flask(__name__)
app.register_blueprint(lab1)

@app.route('/reset_counter')
def reset_counter():
    global count
    count = 0
    return f"""
    <!doctype html>
    <html>
        <body>
            Счётчик очищен <br>
            <a href="{url_for("counter")}">Вернуться к счётчику</a>
        </body>
    </html>
    +"""


@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html> 
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
            </ul>
        </nav>
        <footer>
            <p>Трандышева Алина Константиновна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''


@app.route("/400")
def bad_request():
    return '''<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса</p>
    </body>
</html>''', 400

@app.route("/401")
def unauthorized():
    return '''<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу</p>
    </body>
</html>''', 401

@app.route("/402")
def payment_required():
    return '''<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу</p>
    </body>
</html>''', 402

@app.route("/403")
def forbidden():
    return '''<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к ресурсу запрещен</p>
    </body>
</html>''', 403

@app.route("/405")
def method_not_allowed():
    return '''<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод не разрешен для данного ресурса</p>
    </body>
</html>''', 405

@app.route("/418")
def teapot():
    return '''<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник и не могу заваривать кофе</p>
    </body>
</html>''', 418



@app.route("/server_error")
def server_error():
    result = 10 / 0
    return "Эта строка никогда не будет выполнена"

@app.errorhandler(500)
def internal_server_error(error):
    return '''<!doctype html>
<html>
    <head>
        <title>500 Internal Server Error</title>
    </head>
    <body>
        <h1>500 - Ошибка сервера</h1>
        <p>На сервере произошла внутренняя ошибка</p>
        <p><a href="/">Вернуться на главную страницу</a></p>
    </body>
</html>''', 500

@app.route('/image')
def image():
    path = url_for("static", filename="dog.jpg")
    css_path = url_for("static", filename="lab1.css")
    html_content = f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>Шпиц</h1>
        <img src="{path}">
    </body>
</html>
'''
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-Custom-App': 'Flask-Image-Server',
        'X-Image-Filename': 'dog.jpg',
        'Content-Type': 'text/html; charset=utf-8'
    }



not_found_log = []

@app.route("/404")
def not_found():
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    log_entry = f"{access_time} - {client_ip} - {requested_url}"
    not_found_log.append(log_entry)
    
    image_path = url_for("static", filename="ошибка.webp")
    
    log_html = "<h3>Журнал:</h3>"
    for entry in not_found_log[-5:]:  
        log_html += f"<p>{entry}</p>"
    
    return f'''<!doctype html>
<html>
    <head>
        <title>404 Not Found</title>
        <style>
            body {{
                background: pink;
                color: #333;
                font-family: Arial;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                color: #dc3545;
                font-size: 50px;
            }}
            img {{
                width: 200px;
                margin: 20px;
            }}
            a {{
                color: #007bff;
            }}
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Страница не найдена</p>
        <p><strong>Ваш IP:</strong> {client_ip}</p>
        <p><strong>Время доступа:</strong> {access_time}</p>
        <img src="{image_path}" alt="Not found">
        <p><a href="/">Вернуться на главную страницу</a></p>
        
        {log_html}
        
        <p><small>Всего обращений: {len(not_found_log)}</small></p>
    </body>
</html>''', 404


@app.route('/lab2/a/')
def a():
    return 'ok'

flower_list = [
    {'name': 'роза',      'price': 300},
    {'name': 'тюльпан',   'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка',   'price': 330},
]

@app.route('/lab2/flowers')
def list_flowers():
    return render_template('flower_list.html', flower_list=flower_list)

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    f = flower_list[flower_id]
    return render_template('flower_detail.html',
                           flower_id=flower_id, name=f['name'], price=f['price'])

@app.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    del flower_list[flower_id]
    return redirect(url_for('list_flowers'))

@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('list_flowers'))

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    default_price = 300 + (len(flower_list) % 10) * 10
    flower_list.append({'name': name, 'price': default_price})
    return redirect(url_for('list_flowers'))

@app.route('/lab2/add_flower/')
def add_flower_missing():
    return render_template('flower_missing_400.html'), 400


@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Алина Трандышева', 2, 'ФБИ-34', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                            name=name, lab_num=lab_num, group=group,
                            course=course, fruits=fruits)

@app.route('/lab2/examplebez')
def examplebez():
    return render_template('example.html')


@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
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


@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@app.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    return redirect(f'/lab2/calc/{a}/1')


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

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)


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

@app.route('/lab2/berries')
def show_berries():
    return render_template('berries.html', items=berries)


from flask import send_from_directory

