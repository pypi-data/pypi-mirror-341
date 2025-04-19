from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from qpg.config import Config


config = Config()
engine = create_engine(url=config.get_url())
Session = sessionmaker(bind=engine)


@contextmanager
def get_session(auto_commit=False):
   """
   Контекстный менеджер для работы с сессией базы данных.

   Args:
       auto_commit (bool): Если True, то после выполнения блока кода сессия будет автоматически зафиксирована.

   Yields:
       session: Сессия базы данных.

   Raises:
       Exception: Если возникла ошибка при работе с сессией, то сессия будет откачена.
   """
   session = Session()
   try:
       yield session

       if auto_commit:
           session.commit()
   except Exception as e:
       session.rollback()
   finally:
       session.close()
