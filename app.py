from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'}
        
@app.route("/lab1/author")
def author():
    name = "Трандышева Алина Константиновна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/image')
def image():
    path = url_for("static", filename="dog.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f'''
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

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    reset_url = url_for("reset_counter")

    return f"""
    <!doctype html>
    <html>
        <body>
            Сколько раз вы сюда заходили: {count} <br>
            Дата и время: {time} <br>
            Запрошенный адрес: {url} <br>
            Ваш IP-адрес: {client_ip} <br>
            <a href="{reset_url}">Сбросить счётчик</a>
        </body>
    </html>
"""

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
    """

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/created")
def created():
    return '''
<!doctype html"
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''',201


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
            </ul>
        </nav>
        <footer>
            <p>Трандышева Алина Константиновна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

@app.route("/lab1")
def lab1():
    return '''<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов
веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">Корень сайта</a>
    </body>
</html>'''