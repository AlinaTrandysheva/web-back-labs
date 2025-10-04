from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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
        

@lab1.route("/lab1/author")
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


count = 0

@lab1.route('/lab1/counter')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
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


@lab1.route("/lab1")
def labflask ():
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
         <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главная страница</a></li>
            <li><a href="/index">Index</a></li>
            <li><a href="/lab1/web">Web</a></li>
            <li><a href="/lab1/author">Author</a></li>
            <li><a href="/lab1/counter">Counter</a></li>
            <li><a href="/lab1/info">Info</a></li>
            <li><a href="/created">Created</a></li>
            <li><a href="/image">Image</a></li>
            <li><a href="/400">400 Bad Request</a></li>
            <li><a href="/401">401 Unauthorized</a></li>
            <li><a href="/402">402 Payment Required</a></li>
            <li><a href="/403">403 Forbidden</a></li>
            <li><a href="/404">404 Not Found</a></li>
            <li><a href="/405">405 Method Not Allowed</a></li>
            <li><a href="/418">418 I'm a teapot</a></li>
            <li><a href="/server_error">Server Error (500)</a></li>
        </ul>
        
        <a href="/">Корень сайта</a>
    </body>
</html>'''
