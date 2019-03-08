# test2
тестовое задание

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


## API

для работы с базой пользователей реализовано 4 метода: GET, POST, PUT, DELETE
для демонстрации 3 последних я оформил в форме по адресу:

```
/form 
```

# GET
get - Запрос на 
```
/api/user/id 
```
выдаст информацию о пользователе с заданным id

следующий запрос выведет информацию о всех пользователях в формате json
```
/api/user/0 
```

# POST

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

# DELETE
delete - запрос на 
```
/api/user/
```

