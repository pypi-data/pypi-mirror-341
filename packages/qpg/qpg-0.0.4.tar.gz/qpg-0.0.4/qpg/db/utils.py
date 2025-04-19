from contextlib import contextmanager
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from .models import Base


def init_db(engine):
    Base.metadata.create_all(engine)


@contextmanager
def get_session(engine: Engine, auto_commit=False):
   """
   Контекстный менеджер для работы с сессией базы данных.

   Args:
       auto_commit (bool): Если True, то после выполнения блока кода сессия будет автоматически зафиксирована.

   Yields:
       session: Сессия базы данных.

   Raises:
       Exception: Если возникла ошибка при работе с сессией, то сессия будет откачена.
   """
   Session = sessionmaker(bind=engine)
   session = Session()
   
   try:
       yield session

       if auto_commit:
           session.commit()
   except Exception as e:
       session.rollback()
   finally:
       session.close()