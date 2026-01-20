## FaceOff

Инструмент для анонимизации и обработки видео/изображений с помощью компьютерного зрения. Проект был разработан как решение кейса **НКБ ВС + ИКТИБ ЮФУ** в рамках хакатона **Cyber Garden 18** и занял **1 место**.

![Диплом победителя](media/diplom.jpg)

---

## Стек технологий

| **Слой**             | **Технологии** |
|----------------------|----------------|
| Backend              | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| ML / Computer Vision | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white) |
| Инфраструктура       | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |

---

## Возможности

- **Анонимизация лица** на фото и видео (блюр / маскировка).
- **Выделение объектов** при помощи детектора.
- **REST API** для интеграции с внешними сервисами.
- Возможность контейнеризации и запуска через **Docker Compose**.

---

## Быстрый запуск

Для запуска достаточно установленного **Docker** и **Docker Compose**:

```bash
docker compose up -d --build
```

После старта API будет доступно по адресу `http://127.0.0.1:8000` (Swagger UI: `/docs`).

---

## Структура проекта

```text
FaceOff/
├─ app/
│  ├─ core/                # Базовая конфигурация и безопасность
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  └─ security.py
│  ├─ db/                  # Работа с БД и вспомогательные функции
│  │  ├─ __init__.py
│  │  ├─ database.py
│  │  └─ func.py
│  ├─ ml/                  # ML-логика и взаимодействие с моделями
│  │  ├─ ml_executor.py
│  │  └─ tools/
│  │     ├─ model.py
│  │     ├─ object_detector.py
│  │     └─ write_box.py
│  ├─ routers/             # FastAPI роутеры
│  │  ├─ auth.py
│  │  └─ video.py
│  ├─ schemas/             # Pydantic-схемы
│  │  ├─ uploadfile.py
│  │  └─ user.py
│  ├─ tools/               # Вспомогательные утилиты
│  │  └─ generate_name_file.py
│  ├─ main.py              # Точка входа FastAPI-приложения
│  └─ requirements.txt     # Python-зависимости backend-а
├─ media/
│  └─ diplom.jpg           # Диплом победителя Cyber Garden 18
├─ load_model.py           # Скрипт для подготовки/загрузки модели
├─ docker-compose.yaml     # Оркестрация сервисов
├─ Dockerfile              # Образ приложения
├─ LICENSE
└─ README.md
```

---


