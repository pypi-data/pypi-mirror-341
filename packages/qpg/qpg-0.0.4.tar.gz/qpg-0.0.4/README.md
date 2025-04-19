# QPG: Queue Postgres

Реализует возможность использования Postgres как брокер сообщений.

## Использование

```python
from qpg import PGQueueBase

# Пример использования:

# Cлушаем сообщения
pg_queue = PGQueueBase(session={__здесь_сессия_бд__})
pg_queue.consume()

# Публикуем сообщения
pg_queue = PGQueueBase(session={__здесь_сессия_бд__})
pg_queue.send_message(source="источник сообщения", queue="название очереди", message=dict(data="Привет!"))
```

## Настройка

1. Убедитесь, что у вас установлен PostgreSQL.
2. Создайте базу данных и таблицы, используя модель из `qpg.QueueModel`.

## Структура проекта

```
qpg/
├── __init__.py         # Главный файл инициализации
├── schemas.py          # Схемы данных
└── db/
    ├── __init__.py     
    ├── models.py       # Модели данных
    └── utils.py        # Вспомогательные функции
```

## Установка

```bash
pip install qpg
```

## Лицензия

```
MIT License
```

## Контакты

Для вопросов и предложений: panarin0290@ya.ru

[Купить мне кофе](https://new.donatepay.ru/@1372454)