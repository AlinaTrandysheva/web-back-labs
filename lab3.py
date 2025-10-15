from flask import Blueprint, render_template, request, make_response, redirect, url_for
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'аноним'
    age = request.cookies.get('age') or 'неизвестный'
    name_color = request.cookies.get('name_color') or 'black'
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    return render_template('lab3/form1.html', user=user, age=age, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', type=int, default=0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    fontstyle = request.args.get('fontstyle')

    if color or bgcolor or fontsize or fontstyle:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if fontstyle:
            resp.set_cookie('fontstyle', fontstyle)
        return resp

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    fontstyle = request.cookies.get('fontstyle')

    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        bgcolor=bgcolor,
        fontsize=fontsize,
        fontstyle=fontstyle
    ))
    return resp

@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'GET':
        return render_template('lab3/ticket_form.html', form={}, errors={})

    form = {
        'fio': (request.form.get('fio') or '').strip(),
        'berth': (request.form.get('berth') or '').strip(),
        'linen': request.form.get('linen') == 'on',
        'baggage': request.form.get('baggage') == 'on',
        'age': (request.form.get('age') or '').strip(),
        'from_city': (request.form.get('from_city') or '').strip(),
        'to_city': (request.form.get('to_city') or '').strip(),
        'date': (request.form.get('date') or '').strip(),
        'insurance': request.form.get('insurance') == 'on',
    }

    errors = {}

    if not form['fio']:
        errors['fio'] = 'Укажите ФИО'
    if not form['berth']:
        errors['berth'] = 'Выберите полку'
    if not form['from_city']:
        errors['from_city'] = 'Укажите пункт выезда'
    if not form['to_city']:
        errors['to_city'] = 'Укажите пункт назначения'
    if not form['date']:
        errors['date'] = 'Укажите дату поездки'

    try:
        age_int = int(form['age'])
        if not (1 <= age_int <= 120):
            errors['age'] = 'Возраст должен быть от 1 до 120'
    except ValueError:
        errors['age'] = 'Возраст должен быть числом'

    valid_berths = {
        'нижняя', 'верхняя', 'верхняя боковая', 'нижняя боковая'
    }
    if form['berth'] and form['berth'] not in valid_berths:
        errors['berth'] = 'Недопустимое значение полки'

    if errors:
        return render_template('lab3/ticket_form.html', form=form, errors=errors), 400

    is_child = age_int < 18
    price = 700 if is_child else 1000
    if form['berth'] in ('нижняя', 'нижняя боковая'):
        price += 100
    if form['linen']:
        price += 75
    if form['baggage']:
        price += 250
    if form['insurance']:
        price += 150

    return render_template(
        'lab3/ticket_result.html',
        fio=form['fio'],
        berth=form['berth'],
        linen=form['linen'],
        baggage=form['baggage'],
        age=age_int,
        from_city=form['from_city'],
        to_city=form['to_city'],
        date=form['date'],
        insurance=form['insurance'],
        is_child=is_child,
        price=price
    )


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('fontstyle')
    return resp

