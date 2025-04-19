from datetime import datetime
from pydantic import BaseModel


class QueueSchema(BaseModel):
    """
    Модель схемы очереди.

    Атрибуты:
        source (str): Источник очереди.
        queue_name (str): Имя очереди.
        content (dict): Содержимое очереди.
        state (str): Состояние очереди.
        dt (datetime): Дата и время создания очереди.
    """
    source: str
    queue_name: str
    content: dict
    state: str
    dt: datetime

    class Config:
        """
        Конфигурация модели.

        Атрибуты:
            from_attributes (bool): Флаг, указывающий на использование атрибутов для создания модели.
        """
        from_attributes = True
