# Пример использования Mongo DB в python приложении с [docker-compose](https://docs.docker.com/compose/) конфигурацией

## Краткая информация о проекте
Данный проект является простейшей реализацией бэкенда для приложения TODO-List: приложения, в котором можно создавать, редактировать и удалять TODO карточки.
Проект создан с помощью простого и интуитивного веб-фреймворка для python под названием [Flask](https://flask.palletsprojects.com/en/2.0.x/). Весь проект состоит из одного файла `app.py`, в котором описаны основные endpoints: для вывода полного списка карточек, для вывода только тех карточек, которые ещё не выполнены, и так далее. Также внутри `app.py` находится код инициализации клиента для MongoDB.

*ПРИМЕЧАНИЕ:* данный проект создан исключительно с целью демонстрации использования MongoDB из приложений реализованных на языке `python` и использования `docker-compose` для облегчения процесса локальной разработки. Но в реализации API есть очень спорные моменты (спорные реализации методов, нет консистентности в формате ответов сервера, отсутствие авторизации и аутентификации, и так далее), поэтому данное приложение *не должно* использоваться как есть для реализации какого-либо серьёзного рабочего веб-приложения

### requirements.yml
Данный файл содержит описание [pip](https://pypi.org/project/pip/) пакетов, необходимых для запуска нашего Flask приложения

### Dockerfile
Данный проект включает в себя [Dockerfile](https://docs.docker.com/engine/reference/builder/) - набор инструкций описывающих docker-образ для нашего Flask приложения

### docker-compose.yml
Данный файл содержит описание конфигурации [docker-compose](https://docs.docker.com/compose/). По сути, это описание всех сервисов, которые необходимы для полноценного функционирования нашего приложения и будут запущены в отдельных docker-контейнерах

## Как запустить приложение

### Установка Docker
Для запуска данного приложения вам понадобятся `docker` и `docker-compose`.
Если вы работаете под Windows, `docker` и `docker-compose` находятся внутри `Docker Desktop for Windows` который можно установить [вот таким образом](https://docs.docker.com/desktop/windows/install/).
Если же вы работаете под Linux, вам необходимо отдельно установить пакеты для `docker` и `docker-compose`. Вот как это можно сделать, например, под Ubuntu Linux:
* Установка `docker`: https://docs.docker.com/engine/install/ubuntu/
* Post-install steps для `docker`: https://docs.docker.com/engine/install/linux-postinstall/
* Установка `docker-compose`: https://docs.docker.com/compose/install/

### Запуск приложения
Находясь в папке с приложением просто запустите: `docker-compose up`, это должно повлечь за собой сборку образа для Flask приложения, скачивание образа для `mongo` и запуск пары docker-контейнеров

### Как проверить что приложение работает?
В командной строке (Windows или Linux, тут не так важно) наберите и выполните команды:
* `curl http://localhost:5000/all` - вам в ответ должен вернуться пустой массив: `[]`. Это ожидаемое поведение, поскольку мы не создали ни одной TODO карточки
* `curl -X POST -F 'name=Name' -F 'desc=Desc' -F 'date=2002-02-02' http://localhost:5000/add` - тут вы должны увидеть сообщение `A new card has been added`
* Снова запускаем `curl http://localhost:5000/all` - теперь ответ должен содержать непустой JSON массив с данными только что созданной TODO карточки

## Некоторые сведения о docker и docker-compose
Тут я собрал некоторые статьи, которые помогут вам постичь основы того, чем являются docker контейнеры и образы, и чем они не являются:
- [Что такое Docker: простыми словами о контейнеризации](https://blog.ithillel.ua/articles/chto-takoe-docker-prostymi-slovami-o-konteynerizatsii)
- [Docker-tutorial для новичков. Изучаем докер так, если бы он был игровой приставкой](https://badcode.ru/docker-tutorial-dlia-novichkov-rassmatrivaiem-docker-tak-iesli-by-on-byl-ighrovoi-pristavkoi/)
- [Руководство по docker-compose для начинающих](https://habr.com/ru/company/ruvds/blog/450312/)

Разумеется, основным источником информации является официальная документация по docker и docker-compose, ссылки на которую уже содержатся выше в описании данного проекта