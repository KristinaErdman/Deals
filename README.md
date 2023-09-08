# Результат выполнения тестового задания на позицию Junior Backend разработчик в [Sibdev](https://sibdev.pro/)

Текст задания находится
по [ссылке](https://drive.google.com/drive/folders/1I3Hkf30HoIuJEUfhWXHxGZEJ_K8AYPOh?usp=sharing)

## Первый запуск

1. клонировать данный репозиторий в нужную локальную директорию
   командой ```git clone https://github.com/KristinaErdman/Deals.git```
2. перейти в директорию Deals, содержающую файлы: Dockerfile и docker-compose.yml
3. запустить проект командой ```docker-compose up```
4. применить миграции ```docker exec -it app python manage.py migrate```

## Последующий запуск: ```docker-compose up```

## Работа с сервисом

### 1. Загрузка файла для обработки

**URL:** localhost:8000/api/deals/

**Method:** POST

**Body** (form-data)**:**

- deals: файл, содержащий историю сделок.

**Ответ:**

- файл был обработан без ошибок:

```json
{
  "Status": "OK"
}
```

- в процессе обработки файла произошла ошибка:

```json
{
  "Status": "Error",
  "Desc": <Описание
  ошибки>
}
```

### 2. Выдача обработанных данных

**URL:** localhost:8000/api/customers/top?limit=5

**Method:**  GET

**Ответ:**
В ответе содержится поле “response” со списком из _limit_ клиентов, потративших наибольшую сумму за весь период.

Каждый клиент описывается следующими полями:

- username - логин клиента;
- spent_money - сумма потраченных средств за весь период;
- gems - список из названий камней, которые купили как минимум двое из списка "_limit_ клиентов, потративших наибольшую
  сумму за весь период", и данный клиент является одним из этих покупателей.

**Пример ответа**

```json
{
  "response": [
    {
      "username": "resplendent",
      "spent_money": 451731,
      "gems": [
        "Танзанит",
        "Сапфир",
        "Рубин"
      ]
    },
    ...
  ]
}
```
