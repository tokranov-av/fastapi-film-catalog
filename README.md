# FastAPI Film Catalog 🎬

[![Python checks 🐍](https://img.shields.io/github/actions/workflow/status/tokranov-av/fastapi-film-catalog/python-checks.yaml?branch=master&label=Python%20checks%20%F0%9F%90%8D&logo=github&style=for-the-badge)](https://github.com/tokranov-av/fastapi-film-catalog/actions/workflows/python-checks.yaml)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&style=for-the-badge)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&style=for-the-badge)](https://github.com/psf/black)
[![Lint: Ruff](https://img.shields.io/badge/lint-ruff-%23efc000?logo=ruff&logoColor=white&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Type Checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blueviolet?logo=python&style=for-the-badge)](https://github.com/python/mypy)
[![Dependency: uv](https://img.shields.io/badge/dependencies-uv-4B8BBE?logo=python&style=for-the-badge)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-22C55E?style=for-the-badge&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

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
