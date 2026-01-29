# Проект для обучения разработки высоконагруженных систем

## Требования
- Python 3.4 или выше
- PostgreSQL 15+
- uv (современный менеджер пакетов для Python)
- Docker и Docker Compose (для контейнеризованного запуска)

## Быстрый старт

### Запуск с использованием Docker Compose (рекомендуется)

1. Соберите и запустите проект и все его зависимости:

```bash
docker-compose up --build
```

2. Откройте страничку http://0.0.0.0:8000/docs

### Локальный запуск

1. Установите uv

Для Linux / MacOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Для Windows
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Или с использованием pip:
```bash
pip install uv
```

2. Проверьте, что uv установлен

```bash
uv --version
```

3. Убедитесь что у вас развёрнута СУБД, создан пользователь и БД, скопируйте local.env.example в local.env 
и в POSTGRES_DSN поменяйте необходимые данные

4. Установите зависимости

```bash
make setup
```

5. Запустите приложение

```bash
make start
```

6. Накатите миграции командой

``bash
make migrate
``

7. Откройте страничку http://0.0.0.0:8000/docs