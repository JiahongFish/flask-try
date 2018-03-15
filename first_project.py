from flask import Flask
import flask
from flask import render_template, request, redirect, url_for
import config
from models import User
from extension import db
from flask_pymongo import PyMongo
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mongo = PyMongo(app)


# connect mongodb
def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["address"]
    return handle


# connect elasticsearch
app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200/'
es = Elasticsearch([app.config['ELASTICSEARCH_URL']])


handle = connect()
search_term = ''
pass_res = []
user = handle.users


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        checkUser = User.query.filter(User.username == username, User.password == password).first()
        if checkUser:
            return render_template('search.html', checkUser=checkUser)
        else:
            return 'username or password are not valid'


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        flask.session.clear()
        return flask.redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')

        checkUsername = User.query.filter(User.username == username).first()
        checkEmail = User.query.filter(User.email == email).first()
        if checkUsername:
            return 'Username has been taken'
        elif checkEmail:
            return 'Email wrong'
        else:
            if pwd1 != pwd2:
                return 'please enter same password'
            else:
                user = User(username=username, firstname=firstname, lastname=lastname, email=email,
                            password=pwd1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        return render_template('search.html')
    else:
        search_term = request.form.get('userInput')
        # print(search_term)
        # using search_term to query "_id" from ES
        res = es.search(index='address', size=10, doc_type='users',
                        body={'_source': {'include': '_id'}, 'query': {'multi_match': {'query': search_term,
                                                                                       'fields': ["firstname",
                                                                                                  "lastname", "gender",
                                                                                                  "address", "employer",
                                                                                                  "email", "city",
                                                                                                  "state"]}}})
        hits = res['hits']['hits']
        pass_res = []
        for i in hits:
            if i['_id'] not in pass_res:
                pass_res.append(i['_id'])

        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 10
        end_index = page * 10
        start_index = end_index - per_page;
        pass_result = pass_res[start_index : end_index]
        # users = User.find(...)
        pagination = Pagination(page=page, total=len(pass_res),
                                per_page = 10, record_name='records', show_single_page=True)
        # pagination = Pagination(page=page, total=len(pass_res),
        #                         per_page=10, record_name='records',
        #                         show_single_page=True)
        return render_template("result.html", pass_res=pass_res, pagination=pagination)


@app.route('/<search_id>', methods=['GET', 'POST'])
def detail(search_id):
    details = user.find_one({"_id": search_id})
    firstname = details['firstname']
    lastname = details['lastname']
    gender = details['gender']
    address = details['address']
    employer = details['employer']
    email = details['email']
    city = details['city']
    state = details['state']

    return render_template('detail.html',
                           firstname=firstname,
                           lastname=lastname,
                           gender=gender,
                           address=address,
                           employer=employer,
                           email=email,
                           city=city,
                           state=state)


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()
