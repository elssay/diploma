from app import app, db
from flask import render_template, request
from datetime import datetime
from app.models import Auto, Rentlog


@app.route('/')
def index():
    
    # Получаем все записи из таблицы Auto
    auto_list = Auto.query.all()

    # Полученные наборы передаем в контекст
    context = {
        'auto_list': auto_list,
    }

    return render_template('index.html', **context)


@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():

    context = None

    if request.method == 'POST':
        
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить авто')
        # Получаем название товара - это значение поля input с атрибутом name="title"
        auto_title = request.form['title']

        auto_price = request.form['price']

        auto_description = request.form['description']

        auto_transmission = None

        auto_transmission_check = request.form['transmission']
        if auto_transmission_check == 'option1':
            auto_transmission = True
        elif auto_transmission_check == 'option2':
            auto_transmission = False

        # Добавляем авто в базу данных
        db.session.add(Auto(title=auto_title, autprice=auto_price, description = auto_description, transmission = auto_transmission, astatus = True, img_url=request.form['img_url'], img_url_2=request.form['img_url2'], img_url_3=request.form['img_url3'], img_url_4=request.form['img_url4'], total_price = 0, atotal_time = 0, rent_count = 0))

        # сохраняем изменения в базе
        db.session.commit()
        
        # Заполняем словарь контекста
        context = {
            'method': 'POST',
            'title': auto_title,
            'price': auto_price,
            'description': auto_description,
            'transmission': auto_transmission,
        }
    
    elif request.method == 'GET':

        context = {
            'method': 'GET',
        }

    return render_template('create_auto.html', **context)


@app.route('/auto_detail/<int:auto_id>', methods=['POST', 'GET'])
def auto_detail(auto_id):
    
    auto = Auto.query.get(auto_id) 
    context = None
    free = 'свободен' #статус авто (для Frontend) в зависимости от состояния кнопки "Арендовать/Освободить"
    button_name = 'Арендовать' # название кнопки в зависимости от статуса
    transmission_type = '' # "да" или "нет" в зависимости от того, автоматическая КПП или нет
    
    if auto.astatus == False: #поле таблицы Auto, False - если находится в аренде(занят)
        free = 'занят'
        button_name = 'Освободить'
             
    elif auto.astatus == True:
        free = 'свободен'
        button_name = 'Арендовать'

    if auto.transmission == True:
        transmission_type = 'да'
    elif auto.transmission == False:
        transmission_type = 'нет'
        
    if request.method == 'POST':
        #если нужно изменить информацию об авто:
        new_title = request.form['new_title']
        new_price = request.form['new_price']
        new_description = request.form['new_description']
        auto_transmission_check = request.form['new_transmission'] 
        new_img_url = request.form['new_img_url']
        new_img_url_2 = request.form['new_img_url2']
        new_img_url_3 = request.form['new_img_url3']
        new_img_url_4 = request.form['new_img_url4']
        
        if new_title:
            auto.title = request.form['new_title']
        
        if new_price:
            auto.autprice = request.form['new_price']
        
        if new_description:
            auto.description = request.form['new_description']

        if auto_transmission_check == 'option1': #пользователь выбрал "да" в поле "Автоматическая КПП"
            auto.transmission = True
        elif auto_transmission_check == 'option2': #пользователь выбрал "нет" в поле "Автоматическая КПП"
            auto.transmission = False
              
        if new_img_url:
            auto.img_url = request.form['new_img_url']
        if new_img_url_2:
            auto.img_url_2 = request.form['new_img_url2']
        if new_img_url_3:
            auto.img_url_3 = request.form['new_img_url3']
        if new_img_url_4:
            auto.img_url_4 = request.form['new_img_url4']

        db.session.commit() #сохраняем новую введенную пользователем информацию в поля таблицы БД
  
    #получаем историю аренды для текущего автомобиля:
    rentlog = Rentlog.query.filter_by(auto_id=auto.id).all()
        
    context = {
        'id': auto.id,
        'title': auto.title,
        'price': auto.autprice,
        'description': auto.description,
        'transmission': transmission_type,
        'img_url': auto.img_url,
        'img_url_2': auto.img_url_2,
        'img_url_3': auto.img_url_3,
        'img_url_4': auto.img_url_4,
        'status': free,
        'button_name': button_name,
        'rentlog': rentlog,
    }
    
    return render_template('auto_detail.html', **context)


@app.route('/rent_auto/<int:auto_id>', methods=['POST', 'GET'])
def auto_rent(auto_id): #функция арендовать/освободить авто
    
    auto = Auto.query.get(auto_id)
    context = None
    free = ''
    
    if request.method == 'POST':
        new_status = not auto.astatus

        if new_status == False: #автомобиль свободен
            free = 'занят' #при нажатии на кнопку "Арендовать" статус становится "занят"
            auto.aurented = datetime.now() #записываем время нажатия на кнопку "Арендовать" в поле БД "начало аренды"
            auto.date_end = None #поле "конец аренды" пока пустое
            total_price = 0 #стоимость аренды 
            db.session.commit()

        elif new_status == True:
            free = 'свободен' #автомобиль занят
            auto.date_end = datetime.now() #при нажатии на кнопку "Освободить" в поле "конец аренды" записываем время нажатия на кнопку
            age_seconds = (auto.date_end - auto.aurented).seconds #получаем время аренды в секундах
            age = divmod(age_seconds, 60) #получаем кортеж из минут и секунд времени аренды
            total_price = age[0] * auto.autprice #получаем стоимость аренды, умножив количество минут на стоимость аренды в минуту
            auto.atotal_time += age[0] #добавляем минуты в поле "общее время аренды" авто
            auto.total_price += total_price #добавляем стоимость аренды в поле "общая стоимость аренды" авто
            auto.rent_count +=1 #увеличиваем на 1 общее количесвто бронирований авто

            #добавляем запись об аренде авто в БД:
            db.session.add(Rentlog(auto_id=auto.id, rented = auto.aurented, date_end = auto.date_end, rentprice=total_price))
            db.session.commit()

        auto.astatus = new_status
        db.session.commit()

    context = {
        'id': auto.id,
        'title': auto.title,
        'status': free,
        'auto_status': auto.astatus,
        'arented': auto.arented,
       
    }

    return render_template('rent_auto.html', **context)


@app.route('/del_auto/<int:auto_id>', methods=['POST'])
def del_auto(auto_id): #функция удаления авто
    
    auto = Auto.query.get(auto_id)
    
    context = {
        'id': auto.id,
        'title': auto.title,
        
        }
    
    db.session.delete(auto)
    db.session.commit()

    return render_template('del_auto.html', **context)


@app.route('/rental_log/', methods=['GET'])
def rental_log(): #функция вывода журнала аренды для каждого авто:
    
    auto_list = Auto.query.all()
    
    context = {
        'auto_list': auto_list, 
    }

    return render_template('rental_log.html', **context)

