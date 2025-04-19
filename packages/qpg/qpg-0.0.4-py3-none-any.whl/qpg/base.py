import time
from typing import Any, Generator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from .db.models import Queue
from .schemas import QueueSchema


class PGQueueBase:
    """
    Класс для работы с очередью в PostgreSQL.
    """

    def __init__(self, session: Session):
        self._session = session

    def produce(self, source: str, queue_name: str, message: dict) -> None:
        """
        Добавляет сообщение в очередь.

        :param source: Источник сообщения.
        :param queue_name: Имя очереди.
        :param message: Сообщение для добавления в очередь.
        """
        q = Queue(
            source=source,
            queue_name=queue_name,
            content=message,
        )
        self._session.add(q)

    def consume(self, queue_name: str, source: str | None = None, time_sleep: int = 10) -> Generator[QueueSchema, Any, None]:
        """
        Получает сообщения из очереди.

        :param queue_name: Имя очереди.
        :param source: Источник сообщения (опционально).
        :param time_sleep: Время ожидания перед следующей попыткой получения сообщения (по умолчанию 10 секунд).
        """
        while True:
            q_id = None
            q_schema = None
            processed_successfully = False  # Флаг: успешно ли обработан элемент после yield
            fiters_ = []

            if source:
                fiters_.append(Queue.source == source)

            try:
                try:
                    session = self._session
                    
                    # --- Атомарное получение элемента с блокировкой ---
                    q = (
                        session.query(Queue)
                        .filter(Queue.state == "add", Queue.queue_name == queue_name, *fiters_)
                        .with_for_update(skip_locked=True)
                        .first()
                    )

                    if q is None:
                        # Элементов нет, ждем перед следующей попыткой
                        time.sleep(time_sleep)
                        continue

                    print(f"Received item: id={q.id} source={q.source} queue={q.queue_name}")
                    q_id = q.id  # Сохраняем ID для логирования и последующих операций

                    # --- Валидация данных ---
                    try:
                        q_schema = QueueSchema.model_validate(q)
                    except ValidationError as e:
                        print(f"Validation Error for item {q_id}: {e}")
                        q.state = "error"  # Помечаем как ошибочный при невалидных данных
                        session.commit()
                        # Небольшая пауза после ошибки валидации
                        time.sleep(time_sleep)
                        continue

                    q.state = "processing"  # Помечаем, что элемент взят в обработку
                    session.commit()

                    try:
                        yield q_schema
                        processed_successfully = True
                    except Exception as processing_error:
                        print(
                            f"Error processing item {q_id}: {processing_error}"
                        )  # Ошибка в коде, который получил элемент через yield

                    try:
                        if q and q.state == "processing":  # Проверяем, что статус не изменился
                            if processed_successfully:
                                q.state = "done"
                            else:
                                q.state = "error"

                            session.commit()
                    except SQLAlchemyError as db_error_final:
                        print(
                            f"Failed to update final state for item {q_id}: {db_error_final}"
                        )  # Ошибка при обновлении статуса

                except SQLAlchemyError as db_error:  # Ошибка БД при получении/обработке элемента
                    print(f"Database error during consumption: {db_error}")
                    break  # Прерываем внутренний try, чтобы перейти к паузе

            except Exception as e:  # Другие неожиданные ошибки в цикле
                print(f"Unexpected error in consumer loop: {e}")

            # Пауза если очередь пуста или была ошибка БД/неожиданная ошибка
            if q is None or "db_error" in locals() or "e" in locals():
                del locals()["db_error"]  # Очищаем флаг ошибки БД
                del locals()["e"]  # Очищаем флаг неожиданной ошибки

            time.sleep(time_sleep)
