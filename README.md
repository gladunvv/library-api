# library-api
Web application library, with the possibility of authorization on DRF 


[![Build Status](https://travis-ci.org/gladunvv/library-api.svg?branch=master)](https://travis-ci.org/gladunvv/library-api)
[![codecov](https://codecov.io/gh/gladunvv/library-api/branch/master/graph/badge.svg)](https://codecov.io/gh/gladunvv/library-api)




## Простое API реализующее функционал онлайн-библиотеки на основе Django rest framework

### Содержание:
+ [Краткое описание](#краткое-описание)
+ [Полезные ссылки](#полезные-ссылки)
+ [Requirements](#requirements)
+ [Сборка и запуск проекта](#сборка-и-запуск)
+ [Запросы](#запросы)
  * User
  * Book
  * Genre
  * Author
+ [Особенности](#особенности)
+ [Примеры ответа](#примеры-ответа)
  * [Endpoint 1](#endpoint-1)
  * [Endpoint 2](#endpoint-2)
  * [Endpoint 3](#endpoint-3)
  * [Endpoint 4](#endpoint-4)
+ [License](#license)


### Краткое описание:

Проект представляет собой простое API для поиска и фильтрации данных онлайн-библиотеки. В системе хряаняться данные о Авторах, Жанрах, Книгах. Реализована регистрация через Json Web Token, время жизни токена доступа 15 минут, время жизни токена обновления 7 дней. Неавторизованный пользователь может совершать поиск по названию книги, авторизованному пользователю открывается функционал фильтровации по жанрам и авторам книг. Формат ответа JSON.

### Полезные ссылки:

+ [Django documentation](https://docs.djangoproject.com/en/2.2/)
+ [Django rest framework](https://www.django-rest-framework.org/)
+ [API](https://ru.wikipedia.org/wiki/API)
+ [Simple JWT](https://github.com/davesque/django-rest-framework-simplejwt)

### Requirements:
+ coverage==4.5.4
+ Django==2.2.6
+ django-filter==2.2.0
+ djangorestframework==3.10.3
+ djangorestframework-simplejwt==4.3.0
+ psycopg2==2.8.4
+ PyJWT==1.7.1
+ pytz==2019.3
+ sqlparse==0.3.0

### Сборка и запуск:
! Перед запуском необходимо локально создать и настроить базу данных(Postgresql) а также в корне проекта создать файл .env и заполнить его данными для доступа к базе, пример заполнения в [.env.example](https://github.com/gladunvv/library-api/blob/master/app/.env.example)

```
git clone git@github.com:gladunvv/library-api.git
cd library-api
pip install virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Запросы:
+ User:
  * Create: 
  POST api/v1/users/create/
  * Login:
  POST api/v1/users/login/
  * Delete:
  DELETE api/v1/users/delete/
  * Refresh token:
  POST api/v1/users/token/refresh/


+ Book:
  * Search:
  GET api/v1/onlib/search?search=str
  * Filter:      
  GET api/v1/onlib/filter?genre=pk        
  GET api/v1/onlib/filter?author=pk        
  GET api/v1/onlib/filter?author=pk&genre=pk       
  * View all:
  GET api/v1/onlib/books
  * Create:
  POST api/v1/onlib/books
  * Update:
  PUT api/v1/onlib/books?book=pk
  * Delete:
  DELETE api/v1/onlib/books?book=pk


+ Genre:
  * View all:
  GET api/v1/onlib/genres
  * Create:
  POST api/v1/onlib/genres
  * Update:
  PUT api/v1/onlib/genres?genre=pk
  * Delete:
  DELETE api/v1/onlib/genres?genre=pk


+ Authror:
  * View all:
  GET api/v1/onlib/authors
  * Create:
  POST api/v1/onlib/authors
  * Update:
  PUT api/v1/onlib/authors?author=pk
  * Delete:
  DELETE api/v1/onlib/authors?author=pk


### Особенности:
Касательно Книг, Авторов и Жанров был реализован полный CRUD функционал, где обратиться к безопасным методам (GET) имеет возможность только авторизованный пользователь, а к небезопасным (POST, PUT, DELETE) только пользователь с правами администратора.      
Идентификация:
Для идентификации пользователя в заголовке запроса должен находиться JWT и сопровождаться ключевым словом 'Bearer', которое при необходимости можно сменить на любое другое например, 'Token' или 'JWT' управлять поведением токенов можно при помощи настроек SIMPLE_JWT определенных в [settings.py](https://github.com/gladunvv/library-api/blob/master/app/app/settings.py)
При регистрации и авторизации пользователю отдается два токена **access** и **refresh**, access выступает непосредственно в качестве идентификатора, refresh отдается для обновления access токена.




### Примеры ответа:

### Endpoint 1:   
> POST http://127.0.0.1:8000/api/v1/users/create/        

Тело запроса:
```
{
	"username": "Vladislav",
	"email": "test@email.com",
	"password": "qwerty123"
}
```

Тело отвеа:
```
{
    "id": 1,
    "username": "Vladislav",
    "email": "test@email.com",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTcyODk1NDY5LCJqdGkiOiIyYTBiMGY1YmNlYWU0NTU4ODQ2Yzk5NGM5ZDdmMjhkZSIsInVzZXJfaWQiOjIxfQ.M3TBqtfMLaU__SQIUBQPPL7ExDEOKmQeMtoRARBRHKQ",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3MzQ5OTM2OSwianRpIjoiMDYyMzdkZmYzOGQ3NGRhOWIyNDFkZDIwOTNhY2ViZDgiLCJ1c2VyX2lkIjoyMX0.2oGlLNX3faPaiOMcjEsFVXn3X5QP8U5Wm_mMp3WzwFA"
}
```


### Endpoint 2:
> POST http://127.0.0.1:8000/api/v1/users/token/refresh/         

Тело запроса:
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU3MzQ5OTM2OSwianRpIjoiMDYyMzdkZmYzOGQ3NGRhOWIyNDFkZDIwOTNhY2ViZDgiLCJ1c2VyX2lkIjoyMX0.2oGlLNX3faPaiOMcjEsFVXn3X5QP8U5Wm_mMp3WzwFA"
}
```
Тело ответа:
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTcyODkzNDIyLCJqdGkiOiJiY2M0OWNjYjcyNDM0NzJhODFmZDVmYTIxNDRiMTExOCIsInVzZXJfaWQiOjF9.Po_Vg0prPZX-uy4t9mvFQlAwbZfBPXe-2u0yDKOWJcI"
}
```


### Endpoint 3:
> GET http://127.0.0.1:8000/api/v1/onlib/search?search=Игра        

Тело ответа:
```
[
    {
        "id": 8,
        "title": "Игра в бисер",
        "author": {
            "id": 9,
            "first_name": "Герман",
            "last_name": "Гессе"
        },
        "genre": {
            "id": 11,
            "title": "Роман"
        }
    },
    {
        "id": 9,
        "title": "Игра престолов",
        "author": {
            "id": 10,
            "first_name": "Джордж",
            "last_name": "Мартин"
        },
        "genre": {
            "id": 12,
            "title": "Фэнтези"
        }
    }
]
```


### Endpoint 4:
> GET http://127.0.0.1:8000/api/v1/onlib/filter?author=9     

Заголовок запроса:
```
Authorization Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTcyODkzNDIyLCJqdGkiOiJiY2M0OWNjYjcyNDM0NzJhODFmZDVmYTIxNDRiMTExOCIsInVzZXJfaWQiOjF9.Po_Vg0prPZX-uy4t9mvFQlAwbZfBPXe-2u0yDKOWJcI
```

Тело ответа:
```
[
    {
        "id": 8,
        "title": "Игра в бисер",
        "author": {
            "id": 9,
            "first_name": "Герман",
            "last_name": "Гессе"
        },
        "genre": {
            "id": 11,
            "title": "Роман"
        }
    },
    {
        "id": 10,
        "title": "Сиддхартха",
        "author": {
            "id": 9,
            "first_name": "Герман",
            "last_name": "Гессе"
        },
        "genre": {
            "id": 13,
            "title": "Философский роман"
        }
    }
]
```

### License
This project is licensed under the terms of the MIT license
