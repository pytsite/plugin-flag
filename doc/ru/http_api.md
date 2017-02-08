# PytSite Flag HTTP API


## PATCH flag/toggle/\<model\>/\<uid\>

Установка/снятие отметки для сущности. 


### Аргументы

- `model`. Модель сущности.
- `uid`. UID сущности.


### Параметры
- *required* **str** `access_token`. [Токен доступа](https://github.com/pytsite/pytsite/blob/devel/pytsite/auth/doc/ru/http_api.md).


### Формат ответа

Объект.

- **bool** `status`. Состояние флага для данного пользователя. `true` -- установлен, `false` -- снят.
- **int** `count`. Общее количество установленных флагов для сущности.


### Примеры

Запрос:

```
curl -X PATCH \
-d access_token=77aaea01a5e58ac3a7d114f418231fa6 \
http://test.com/api/1/flag/toggle/article/57a304e2523af552d17a4dfb
```


Ответ:
```
{
    "status": true,
    "count": 728
}
```


## Смотрите также

- [PytSite HTTP API](https://github.com/pytsite/pytsite/blob/devel/pytsite/http_api/doc/ru/index.md)
