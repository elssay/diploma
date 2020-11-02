from app import app, db
from flask import render_template, request
from app.models import Auto


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
        db.session.add(Auto(title=auto_title, price=auto_price, description = auto_description, transmission = auto_transmission, status = True, img_url=request.form['img_url']))

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

        # Пришел запрос с методом GET - пользователь просто открыл в браузере страницу по адресу http://127.0.0.1:5000/create_product
        # В этом случае просто передаем в контекст имя метода
        context = {
            'method': 'GET',
        }

    return render_template('create_auto.html', **context)

@app.route('/auto_detail/<int:auto_id>', methods=['POST', 'GET'])
def auto_detail(auto_id):
    
    auto = Auto.query.get(auto_id)


    context = None
    free = ''
    button_name = ''
    if auto.status == False:
        free = 'Занят'
        button_name = 'Освободить'
    elif auto.status == True:
        free = 'свободен'
        button_name = 'Арендовать'
   
    if request.method == 'POST':

        new_title = request.form['new_title']
        new_price = request.form['new_price']
        new_description = request.form['new_description']
        auto_transmission_check = request.form['new_transmission'] 
        new_img_url = request.form['new_img_url']

        if new_title:
            auto.title = request.form['new_title']
        
        if new_price:
            auto.price = request.form['new_price']
        
        if new_description:
            auto.description = request.form['new_description']


        if auto_transmission_check == 'option1':
            auto.transmission = True
        elif auto_transmission_check == 'option2':
            auto.transmission = False
              
        if new_img_url:
            auto.img_url = request.form['new_img_url']

        
        #db.session.commit() 

    

    context = {
        'method': 'POST',
        'id': auto.id,
        'title': auto.title,
        'price': auto.price,
        'description': auto.description,
        'img_url': auto.img_url,
        'status': free,
        'button_name': button_name,
    }
    db.session.commit() 


    return render_template('auto_detail.html', **context)


@app.route('/rent_auto/<int:auto_id>', methods=['POST'])
def auto_rent(auto_id):
    
    auto = Auto.query.get(auto_id)

    context = None
    free = ''
    new_status = not auto.status

    if new_status == False:
        free = 'занят'
        
    elif new_status == True:
        free = 'свободен'
        
    auto.status = new_status
    #db.session.commit()

    context = {
        'id': auto.id,
        'title': auto.title,
        'status': free,
        'auto_status': auto.status,
    }

    db.session.commit()


    return render_template('rent_auto.html', **context)



@app.route('/del_auto/<int:auto_id>', methods=['POST'])
def del_auto(auto_id):
    
    auto = Auto.query.get(auto_id)

    context = {
        'method': 'POST',
            'id': auto.id,
            'title': auto.title,
            'price': auto.price,
            'description': auto.description,
            'status': auto.status,
            'transmission': auto.transmission,
    }
    
    db.session.delete(auto)
    db.session.commit()

    return render_template('del_auto.html', **context)


