# Каталог фильмов разработанный на фреймворке FastAPI

## Разработка

После push в репозиторий, проверьте GItHub Actions

### Установка

Если работаете в IDE PyCharm, директорию film-catalog отметьте как "Sources Root":

Выделите директорию -> Нажмите правую кнопку мыши -> Mark Directory as -> Sources Root

Установка зависимостей:
```shell
uv install
```

### Конфигурация pre-commit

Установка pre-commit хук:
```shell
pre-commit install
```

### Запуск

Перейдите в директорию film-catalog:
```shell
cd film-catalog
```

Запуск сервера dev
```shell
fastapi dev
```

## Сниппеты

```shell
python -c 'import secrets; print(secrets.token_urlsafe(16))'
```
