# FastAPI Film Catalog 🎬

[![Python checks 🐍](https://img.shields.io/github/actions/workflow/status/tokranov-av/fastapi-film-catalog/python-checks.yaml?branch=master&label=Python%20checks%20%F0%9F%90%8D&logo=github&style=for-the-badge)](https://github.com/tokranov-av/fastapi-film-catalog/actions/workflows/python-checks.yaml)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&style=for-the-badge)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&style=for-the-badge)](https://github.com/psf/black)
[![Lint: Ruff](https://img.shields.io/badge/lint-ruff-%23efc000?logo=ruff&logoColor=white&style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Type Checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blueviolet?logo=python&style=for-the-badge)](https://github.com/python/mypy)
[![Dependency: uv](https://img.shields.io/badge/dependencies-uv-4B8BBE?logo=python&style=for-the-badge)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-22C55E?style=for-the-badge&logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2Ftokranov-av%2F097eab66890510888aa7d0e190361e03%2Fraw%2Fcoverage.json&style=for-the-badge)](https://github.com/tokranov-av/fastapi-film-catalog/actions/workflows/python-checks.yaml)

## Разработка

### ⚙️ Подготовка к работе

1. Установите `docker`, `pyenv`, `pipx` в соответствии с их документациями.
2. C помощью `pyenv` установите версию `python`, указанную в файле `.python-version`, например:
```shell
pyenv install 3.13.7
pyenv global 3.13.7
```
3. Установите `Black` глобально с помощью `uv`:
```shell
uv tool install black
```
4. Склонируйте проект и перейдите в его директорию, в моем случае:
```shell
git clone git@github.com:tokranov-av/fastapi-film-catalog.git && cd fastapi-film-catalog
```
5. Установите зависимости (включая dev-зависимости):
```shell
uv sync --dev
```
6. В активированном виртуальном окружении установите `pre-commit` хук:
```shell
pre-commit install
```

Если работаете в IDE PyCharm:

1. Директорию `film-catalog` отметьте как `Sources Root`:
Выделите директорию ➡️ Нажмите правую кнопку мыши ➡️ `Mark Directory as` ➡️ `Sources Root`
2. Установите интерпретатор для проекта (после установки зависимостей в папке с проектом должна создастся папка `.venv` с зависимостями).
3. Включите `Black` в PyCharm в разделе `Tools`. При включении в выпадающем списке `Execution mode` выберете `binary`, в поле `Black executable` укажите ссылку на глобально установленный `Black`.

---


Запуск Redis

```shell
docker volume create fastapi-film-catalog
docker container run --name redis-film-catalog -d -p 6379:6379 -v fastapi-film-catalog:/data redis
```


### 🔍 Проверка с помощью Ruff

Текущую директорию:
```shell
ruff check .
```
Конкретный файл:
```shell
ruff check path/to/file.py
```
С автоматическим исправлением:
```shell
ruff check --fix .
```
---

### 🔍 Проверка с помощью mypy

Текущую директорию:
```shell
mypy .
```
Конкретный файл:
```shell
mypy path/to/file.py
```
---

### ✅ Запуск тестов

Запустите redis в контейнере docker (временное решение, пока используется только redis в проекте):
```shell
docker container run --name redis-film-catalog-tests -d -p 6380:6379 redis
```
**Запуск тестов в виртуальном окружении**

В терминале перейдите в директорию `fastapi-film-catalog`, после чего:
- активируйте виртуальное окружение (ОС Ubuntu 24.04): `source .venv/bin/activate`
- добавьте переменные окружения: `export TESTING=1` и `export REDIS_PORT=6380`
- запустите тесты: `pytest -v`

**Запуск тестов через uv**

В директории `fastapi-film-catalog` выполните команду `TESTING=1 REDIS_PORT=6380 uv run pytest -v`

---

### Процесс внесения изменений

1.  Сделайте `fork` репозитория.
2.  Создайте ветку для вашей фичи (`git checkout -b feature/amazing-feature`).
3.  Закоммитьте изменения (`git commit -m 'Add some amazing feature'`).
4.  Запушьте ветку (`git push origin feature/amazing-feature`).
5.  После `push` в репозиторий, обязательно проверьте статус запуска пайплайна в **GitHub Actions**
6.  Откройте `Pull Request`.

---

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
