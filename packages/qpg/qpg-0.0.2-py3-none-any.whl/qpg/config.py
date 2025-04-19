import os
from pydantic import BaseModel
from sqlalchemy import URL


class Config(BaseModel):
    """
    Класс конфигурации для подключения к базе данных.
    """
    drivername: str = os.getenv("drivername", "postgresql+psycopg2")
    host: str = os.getenv("host", "localhost")
    port: int = os.getenv("port", 5432)
    username: str = os.getenv("username", "postgres")
    password: str = os.getenv("password", "postgres")
    database: str = os.getenv("database", "postgres")

    def get_url(self):
        """
        Метод для создания URL подключения к базе данных.

        Returns:
            URL: Объект URL для подключения к базе данных.
        """
        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
