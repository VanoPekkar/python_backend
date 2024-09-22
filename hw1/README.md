# Как запускать

### 1. Создание виртуального окружения (опционально)

```
python -m venv venv

source venv/bin/activate (Linux/MacOS)
venv\Scripts\activate.bat (Windows)
```

### 2. Установка зависимостей

```
pip install -r requirements.txt
```

### 3. Запуск приложения

```
python -m uvicorn app.main:app
```