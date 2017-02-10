# PytSite Flag HTTP API


## PATCH flag/\<flag_type\>/\<model\>/\<uid\>

Установка/снятие флага для сущности. 


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Параметры
- *required* **str** `access_token`. [Токен доступа](https://github.com/pytsite/pytsite/blob/devel/pytsite/auth/doc/ru/http_api.md).


### Формат ответа

Объект.

- **bool** `status`. Состояние флага для данного пользователя: `true` -- установлен, `false` -- снят.


### Примеры

Запрос:

```
curl -X PATCH \
-d access_token=77aaea01a5e58ac3a7d114f418231fa6 \
http://test.com/api/1/flag/like/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "status": true
}
```


## GET flag/count/\<flag_type\>/\<model\>/\<uid\>

Получение количества установленных флагов для сущности.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Параметры
- *required* **str** `access_token`. [Токен доступа](https://github.com/pytsite/pytsite/blob/devel/pytsite/auth/doc/ru/http_api.md).


### Формат ответа

Объект.

- **int** `count`. Общее количество установленных флагов для сущности.


### Примеры

```
curl -X GET \
-d access_token=77aaea01a5e58ac3a7d114f418231fa6 \
http://test.com/api/1/flag/count/like/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "count": 624
}
```


## GET flag/status/\<flag_type\>/\<model\>/\<uid\>

Получение статуса флага для сущности для текущего пользователя.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Параметры
- *required* **str** `access_token`. [Токен доступа](https://github.com/pytsite/pytsite/blob/devel/pytsite/auth/doc/ru/http_api.md).


### Формат ответа

Объект.

- **bool** `status`. Статус флага для текущего пользователя: `true` -- установлен, `false` -- снят.


### Примеры

```
curl -X GET \
-d access_token=77aaea01a5e58ac3a7d114f418231fa6 \
http://test.com/api/1/flag/status/like/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "status": true
}
```
