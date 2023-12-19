# Профили пользователей онлайн-кинотеатра

В настоящем репозитории реализован сервис профилей пользователей нашего онлайн-кинотеатра.
Он представляет собой веб-приложение написанное на fastAPI, предоставляющее возможность:
#### при работе с профилями пользователей
+ 1.1. Добавлять и обновлять персональные данные пользователя;
+ 1.2. Получать информацию о пользователе;
#### работая с коллекциями фильмов,
+ 2.1. Посмотреть фильмы, которые пользователь поместил в закладки;
+ 2.2. Посмотреть фильмы, которым пользователь поставил лайк;
+ 2.3. Посмотреть историю просмотров пользователя;
+ 2.4. Посмотреть детальную информацию о фильме (включая общие UGC (комментарии, лайки, рецензии) и UGC пользователя);
#### работая с закладками,
+ 3.1. Добавить фильм в закладки;
+ 3.2. Удалить фильм из закладок;
#### при просмотре фильма
+ 4.1. Сохранить момент в фильме, до которого пользователь успел досмотреть (другими словами: позваляет сохранить прогресс просмотра);
#### работая с рецензиями,
+ 5.1. Оставить рецензию на фильм;
+ 5.2. Удалить рецензию на фильм;
+ 5.3. Обновить рецензию на фильм;
+ 5.4. Прочесть все рецензии на фильм;
#### посмотрев фильм или прочитав рецензию,
+ 6.1. Поставить фильму лайк;
+ 6.2. Забрать у фильма свой лайк;
+ 6.3. Поставить рецензии лайк;
+ 6.4. Забрать у рецензии свой лайк;
+ 6.5. Посмотреть все лайки, поставленные фильму;
+ 6.6. Посмотреть все лайки, поставленные рецензии;

# Запуск сервиса пользовательских профилей
### Запуск в составе docker compose
Настоящий сервис взаимодействует с двумя другими сервисами проекта онлайн-кинотеатра: movies_api и auth_api. Первый должен быть поднят с использованием его [репозитория](https://github.com/chingisdev/Async_API_sprint_2) (следуя справке, находящейся в том же репозитории), auth_api указан в docker-compose.yml настоящего репозитория. 
Заполните файл .ugc.env.development согласно образцу .ugc.env.development.example и запустите контейнеры проекта:
```
docker compose up -d
```
### Запуск в production
должен осуществляться из [deploy-репозитория](https://github.com/allyotov/graduate_work), в котором сконфигурированы все контейнеры проекта онлайн-кинотеата (справку можно найти там же).

### Локальный запуск для отладки

Для локального отладочного запуска сервиса вам понадобится пакетный менеджер и созданное виртуальное окружение.
В текущей мажорной версии сервиса используется пакетный менеджер pip.
В [work-in-progress-версии с тестами](https://github.com/chingisdev/practicum_profile_API/tree/a.lyotov/feat/test-profiles) используется poetry.
## I.A. venv и pip
создайте виртуальное окружение:
```bash
python -m venv .\venv\
```
активируйте виртуальное окружение:

A. Linux:
```bash
$ source ./venv/bin/activate
```
B. Windows:
```bash
.\venv\Scripts\activate.bat
```
установите зависимости:
```bash
pip install -r requirements.txt
```
## I.B. poetry
##### NB. В системе должен быть установлен менеджер python-пакетов poetry!
создайте виртуальное и активируйте окружение:
```bash
poetry shell
```
ecли необходимо, установите явно зависимости проекта:
```bash
poetry install
```
Далее можно воспользоваться debugger'ом вашей IDE или написать таргет в Makefile. Переменные из env-файла .ugc.env.development должны быть предварительно экспортированы в переменные окружения (этом можно сделать либо средствами IDE, либо конструкцией include в начале Makefile'а)
# Profile API
### 1.1. Добавлять и обновлять персональные данные пользователя:
```
PATCH localhost:80/profile/api/v1/profile
```
### 1.2. Получать информацию о пользователе:
```
GET localhost:80/profile/api/v1/profile
```
### 2.1. Посмотреть фильмы, которые пользователь поместил в закладки:
```
GET localhost:80/profile/api/v1/collection/bookmarks
```
### 2.2. Посмотреть фильмы, которым пользователь поставил лайк:
```
GET localhost:80/profile/api/v1/collection/likes
```
### 2.3. Посмотреть историю просмотров пользователя:
```
GET localhost:80/profile/api/v1/collection/history
```
### 2.4. Посмотреть детальную информацию о фильме:
#### (включая общие UGC: комментарии, лайки, рецензии; и UGC пользователя)
```
GET localhost:80/profile/api/v1/collection/movie/{movie_id}
```
### 3.1. Добавить фильм в закладки:
```
POST localhost:80/profile/api/v1/bookmark/{movie_id}
```
### 3.2. Удалить фильм из закладок:
```
DELETE localhost:80/profile/api/v1/bookmark/{movie_id}
```
### 4.1. Сохранить момент в фильме, до которого пользователь успел досмотреть:
##### (другими словами: сохранить прогресс просмотра) 
```
POST localhost:80/profile/api/v1/progress
```
### 5.1. Оставить рецензию на фильм:
```
POST localhost:80/profile/api/v1/review/{movie_id}
```
### 5.2. Удалить рецензию на фильм:
```
DELETE localhost:80/profile/api/v1/review/delete-review
```
### 5.3. Обновить рецензию на фильм:
```
PATCH localhost:80/profile/api/v1/review/update/{review_id}
```
### 5.4. Прочесть все рецензии на фильм:
```
GET localhost:80/profile/api/v1/review/{movie_id}
```
### 6.1. Поставить фильму лайк:
```
POST localhost:80/profile/api/v1/like/movie/{movie_id}
```
### 6.2. Забрать у фильма свой лайк:
```
DELETE localhost:80/profile/api/v1/like/movie/{movie_id}
```
### 6.3. Поставить рецензии лайк:
```
POST localhost:80/profile/api/v1/like/review/{review_id}
```
### 6.4. Забрать у рецензии свой лайк:
```
DELETE localhost:80/profile/api/v1/like/review/{review_id}
```
### 6.5. Посмотреть все лайки, поставленные фильму:
```
GET localhost:80/profile/api/v1/like/movie/{movie_id}
```
### 6.6. Посмотреть все лайки, поставленные рецензии:
```
GET localhost:80/profile/api/v1/like/review/{review_id}
```
# Функциональные тесты Profile API
находятся в настоящий момент в разработке на стадии завершения подготовки необходимой инфраструктуры. Работа над ними ведётся в [отдельной feature-ветке настоящего репозитория](https://github.com/chingisdev/practicum_profile_API/tree/a.lyotov/feat/test-profiles).