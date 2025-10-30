from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('lab4/div.html', error="Введите оба числа!")

    x1 = float(x1)
    x2 = float(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error="Ошибка: делить на ноль незлья")

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    x1 = float(x1) if x1 else 0
    x2 = float(x2) if x2 else 0

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    x1 = float(x1) if x1 else 1
    x2 = float(x2) if x2 else 1

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        return render_template('lab4/sub.html', error="Ошибка: оба поля должны быть заполнены!")

    x1 = float(x1)
    x2 = float(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/vozv-form')
def vozv_form():
    return render_template('lab4/vozv-form.html')



@lab4.route('/lab4/vozv', methods=['POST'])
def vozv():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        return render_template('lab4/vozv.html', error="Ошибка: оба поля должны быть заполнены!")

    x1 = float(x1)
    x2 = float(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/vozv.html', error="Ошибка: 0 в степени 0 — нельзя")

    result = x1 ** x2
    return render_template('lab4/vozv.html', x1=x1, x2=x2, result=result)


tree_count = 0
MAX_TREES = 10

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'POST':
        operation = request.form.get('operation')

        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < MAX_TREES:
            tree_count += 1

        return redirect('/lab4/tree')

    return render_template('lab4/tree.html', tree_count=tree_count, max_trees=MAX_TREES)


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алекс Уиллер', 'gender': 'm'},
    {'login': 'bob',  'password': '555', 'name': 'Боб Джекович',     'gender': 'm'},
    {'login': 'lin',  'password': '039', 'name': 'Лина Трандышева',    'gender': 'f'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            current_login = session['login']
            user = next((u for u in users if u['login'] == current_login), None)
            if user:
                return render_template('lab4/login.html', authorized=True, login=user['login'], name=user['name'])
        
        return render_template('lab4/login.html', authorized=False, login='')

    login_value = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not login_value:
        return render_template(
            'lab4/login.html', authorized=False, error='Не введён логин', login=login_value)
    
    if not password:
        return render_template('lab4/login.html', authorized=False, error='Не введён пароль', login=login_value)

    for user in users:
        if login_value == user['login'] and password == user['password']:
            session['login'] = login_value
            return render_template('lab4/login.html', authorized=True, login=login_value, name=user['name'], success='Успешная авторизация')

    return render_template('lab4/login.html', authorized=False, error='Неверные логин или пароль', login=login_value)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = None
    snowflakes = 0
    temp_value = ''

    if request.method == 'POST':
        temp = request.form.get('temperature')
        temp_value = temp

        if not temp:
            message = 'Ошибка: не задана температура'
        else:
            try:
                t = float(temp)

                if t < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif t > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= t <= -9:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 3
                elif -8 <= t <= -5:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 2
                elif -4 <= t <= -1:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 1
            except ValueError:
                message = 'Ошибка: температура должна быть числом'

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temp_value)


