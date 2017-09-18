# PytSite Flag HTTP API

Каждый запрос обязательно должен включать заголовок [аутентификации](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md#%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D0%BE%D0%B2).


## POST flag/:flag_type/:model/:uid

Установка флага.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Формат ответа

Объект.

- **int** `count`. Общее количество установленных флагов для сущности.


### Примеры

Запрос:

```
curl -X POST \
-H 'PytSite-Auth: 77aaea01a5e58ac3a7d114f418231fa6' \
http://test.com/api/1/flag/like/article/57a304e2523af552d17a4dfb
```

Ответ:

```
{
    "count": 123
}
```


## GET flag/:flag_type/:model/:uid

Получение текущего состояния флага.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Формат ответа

Объект.

- **bool** `status`. Состояние флага: `true` -- установлен, `false` -- снят.


### Примеры

```
curl -X GET \
-H 'PytSite-Auth: 77aaea01a5e58ac3a7d114f418231fa6' \
http://test.com/api/1/flag/status/like/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "status": true
}
```

## PATCH flag/:flag_type/:model/:uid

Смена состояния флага на противоположное.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Формат ответа

Объект.

- **int** `count`. Общее количество установленных флагов для сущности.
- **bool** `status`. Текущее состояние флага: `true` -- установлен, `false` -- снят.


### Примеры

Запрос:

```
curl -X PATCH \
-H 'PytSite-Auth: 77aaea01a5e58ac3a7d114f418231fa6' \
http://test.com/api/1/flag/like/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "count": 123,
    "status": true
}
```



## DELETE flag/:flag_type/:model/:uid

Удаление флага.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Формат ответа

Объект.

- **int** `count`. Общее количество установленных флагов для сущности.


### Примеры

Запрос:

```
curl -X DELETE \
-H 'PytSite-Auth: 77aaea01a5e58ac3a7d114f418231fa6' \
http://test.com/api/1/flag/like/article/57a304e2523af552d17a4dfb
```

Ответ:
```
{
    "count": 123
}
```


## GET flag/count/:flag_type/:model/:uid

Получение общего количества установленных флагов.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.
- `uid`. UID сущности.


### Формат ответа

- **int** `count`. Общее количество установленных флагов для сущности.


### Примеры

```
curl -X GET \
-H 'PytSite-Auth: 77aaea01a5e58ac3a7d114f418231fa6' \
http://test.com/api/1/flag/count/like/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "count": 123
}
```


## GET flag/entities/:flag_type/:model

Получение сущностей, отмеченным флагом.


### Аргументы

- `flag_type`. Тип флага.
- `model`. Модель сущности.


### Параметры

- `count`. Количество возвращаемых сущностей. Значение по
  умолчанию: 100. Максимальное значение: 100.
- `skip`. Количество пропускаемых сущностей. Значение по
  умолчанию: 0.


### Формат ответа

Список сущностей.


### Примеры

```
curl -X GET \
-H 'PytSite-Auth: 77aaea01a5e58ac3a7d114f418231fa6' \
http://test.com/api/1/flag/entities/like/article
```


Ответ:
```
[
...
]
```
