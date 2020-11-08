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

        # Получаем цену товара - это значение поля input с атрибутом name="price"
        auto_price = request.form['price']

        auto_description = request.form['description']

        auto_transmission = None

        auto_transmission_check = request.form['transmission']
        if auto_transmission_check == 'option1':
            auto_transmission = True
        elif auto_transmission_check == 'option2':
            auto_transmission = False

    

        # Добавляем авто в базу данных
        db.session.add(Auto(title=auto_title, autprice=auto_price, description = auto_description, transmission = auto_transmission, astatus = True, img_url=request.form['img_url'], total_price = 0, atotal_time = 0, rent_count = 0))

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
    free = 'свободен'
    button_name = 'Арендовать'
    
    if auto.astatus == False:
        free = 'занят'
        button_name = 'Освободить'
        #agelist.append(auto.auend_of_rent.strftime("%Y-%m-%d-%H.%M.%S"))
        
    elif auto.astatus == True:
        free = 'свободен'
        button_name = 'Арендовать'
        #agelist.append(auto.aurented.strftime("%Y-%m-%d-%H.%M.%S"))
    if request.method == 'POST':

        new_title = request.form['new_title']
        new_price = request.form['new_price']
        new_description = request.form['new_description']
        auto_transmission_check = request.form['new_transmission'] 
        new_img_url = request.form['new_img_url']
        

        if new_title:
            auto.title = request.form['new_title']
        
        if new_price:
            auto.aprice = request.form['new_price']
        
        if new_description:
            auto.description = request.form['new_description']


        if auto_transmission_check == 'option1':
            auto.transmission = True
        elif auto_transmission_check == 'option2':
            auto.transmission = False
              
        if new_img_url:
            auto.img_url = request.form['new_img_url']
        db.session.commit() 

    

    rentlog = Rentlog.query.filter_by(auto_id=auto.id).all()
        
    

    context = {
        'id': auto.id,
        'title': auto.title,
        'price': auto.autprice,
        'description': auto.description,
        'img_url': auto.img_url,
        'status': free,
        'button_name': button_name,
        'rentlog': rentlog,
    }
    #db.session.commit() 


    return render_template('auto_detail.html', **context)


@app.route('/rent_auto/<int:auto_id>', methods=['POST', 'GET'])
def auto_rent(auto_id):
    
    auto = Auto.query.get(auto_id)
    
    context = None
    free = ''
    
    if request.method == 'POST':
        new_status = not auto.astatus
        if new_status == False:
            free = 'занят'
            auto.aurented = datetime.now()
            #auto.auend_of_rent = None
            #l = auto.aurented.strftime("%Y-%m-%d-%H.%M.%S")
        elif new_status == True:
            free = 'свободен'
            auto.auend_of_rent = datetime.now()
            

        auto.astatus = new_status
        auto.rent_count+=1
        age_seconds = (auto.auend_of_rent - auto.aurented).seconds
        age = divmod(age_seconds, 60)
        total_price = age[0] * auto.autprice
        auto.atotal_time += age[0]
        auto.total_price += total_price

        db.session.add(Rentlog(auto_id=auto.id, rented = auto.aurented, end_of_rent = auto.auend_of_rent, rentprice=total_price))
        db.session.commit()

    context = {
        'id': auto.id,
        'title': auto.title,
        'status': free,
        'auto_status': auto.astatus,
        'arented': auto.arented,
        'aend_of_rent': auto.aend_of_rent,
        'time': auto.arented,
    }

    return render_template('rent_auto.html', **context)



@app.route('/del_auto/<int:auto_id>', methods=['POST'])
def del_auto(auto_id):
    
    auto = Auto.query.get(auto_id)
    

    context = {
        'id': auto.id,
        'title': auto.title,
        'price': auto.autprice,
        'description': auto.description,
        'astatus': auto.status,
        'status': auto.astatus,
        'transmission': auto.transmission,
        'id': auto.id,
        'arented': auto.aurented,
        'aend_of_rent': auto.auend_of_rent,
        }
    
    db.session.delete(auto)
    db.session.commit()

    return render_template('del_auto.html', **context)


@app.route('/rental_log/', methods=['GET'])
def rental_log():
    
    auto_list = Auto.query.all()
    #auto = Auto.query.get(auto_id)

  
    # Полученные наборы передаем в контекст
    context = {
        # 'title': auto.title,
        'auto_list': auto_list,
        # 'count':auto.rent_count,
        # 'total_time': auto.total_time,
        # 'total_price': auto.total_price,
    }

    return render_template('rental_log.html', **context)

