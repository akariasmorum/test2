# test2
тестовое задание

преамбула: я пытался упаковать nginx в контейнер, но localhost выдает 502 Bad Gateway. Шел 2ой день востания машин, преимущество на их стороне 

данное руководство по развертыванию подразумевает, что у вас уже установлен nginx и docker-compose

## настройка докера

клонировать репозиторий:
```
git clone https://github.com/akariasmorum/test2.git
```

перейти в папку
```
cd test2
```

собираем docker
```
sudo docker-compose build
```

поднимаем его
```
sudo docker-compose up
```

## настройка nginx:

создать файл `test.conf` в
```
etc/nginx/sites-available/
```

и добавить в него
```
server {
    listen 80;
    server_name 127.0.0.1;
 
    root ~/git/test2/run.py;
  
    access_log access.log;
    error_log errors.log;

    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://0.0.0.0:8001;
            break;
        }
    }
}
```
переходим на уровень выше в
```
usr/nginx/
```
и в файле `nginx.conf` **в раздел `http`** добавляем

```
include /etc/nginx/sites-enabled/test.conf;
```


Cоздать файлы `access.log` и `errors.log` в
```
usr/share/nginx
```

проверить nginx:
```
sudo nginx -t
```

перезагрузить nginx:
```
sudo service nginx restart
```

перейти на `http://localhost`


# API

для работы с базой пользователей реализовано 4 метода: GET, POST, PUT, DELETE
для демонстрации 3 последних я оформил в форме по адресу:

```
/form 
```
**результат выполнения на них выводится в консоль**

### GET
get - Запрос на 
```
/api/user/id 
```
выдаст информацию о пользователе с заданным id

следующий запрос выведет информацию о всех пользователях в формате json
```
/api/user/0 
```

### POST

post на
```
/api/user/
```
добавляет указанных пользователей в базу. например:
```
[
	{"username": "Jaclyn", "name": "Jaclyn", "password": "spsNBDKg"},
	{"username": "Neville", "name": "Neville", "password": "NehqUPvR"},
	{"username": "Janey", "name": "Janey", "password": "8pCMsS5d"},
	{"username": "Jerrics", "name": "Jerrics", "password": "7Lb3a5hm"},
	{"username": "Monte", "name": "Monte", "password": "2nhXZ8U6"}
]
```
### PUT
put на
```
/api/user/
```
обновляет информацию о пользователях. например:
```
[
	{"id": "5", "name": "Michelangelo"},
	{"id": "6", "name": "Donatello"}
]
```
обновит информацию о пользователях с id 5 и 6

### DELETE
delete - запрос на 
```
/api/user/
```
удаляет указанных пользователей. например:
```
[
	{"username": "Jaclyn"},
	{"username": "Neville"},
	{"username": "Janey"},
	{"username": "Jerrics"},
	{"username": "Monte"}
]
```

раз уж вы здесь,то вы меня спрашивали "есть ли в списке повторяющиеся элементы". я предложил циклами, вы предложили set'ом.
так вот, я провел исследование. результаты неоднозначны. может это баг, а может и фича
перейдите на jupiter notebook
'''
https://mybinder.org/v2/gh/ipython/ipython-in-depth/master?filepath=binder/Index.ipynb
'''
file -> open. появится новое окно -> справа upload
выберите ipynb (2).ipynb  который лежит здесь, в корне репозитория
