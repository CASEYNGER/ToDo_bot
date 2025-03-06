from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncAttrs, async_sessionmaker, create_async_engine
)

from config import DB_URL

# Создание асинхронного движка
engine = create_async_engine(
    url=DB_URL,
    echo=True
)

# Создание фабрики сессий для выполнения запросов в БД
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей.

    AsyncAttrs делает модель асинхронно-совместимой.
    """
    pass


class User(Base):
    """Пользователь Telegram."""
    # Название таблицы
    __tablename__ = 'users'

    # Автоинкрементный первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # Идентификатор пользователя
    telegram_id = mapped_column(BigInteger)


class Task(Base):
    """Задача пользователя Telegram."""
    # Название таблицы
    __tablename__ = 'tasks'

    # Автоинкрементный первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    # Текст задачи (максимум 100 символов)
    task: Mapped[str] = mapped_column(String(100))
    # Внешний ключ, связывающий задачу с пользователем
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))


async def async_main():
    """Создание таблиц в БД."""
    # Асинхронное соединение с БД
    async with engine.begin() as conn:
        # Создаем таблицы, если их еще нет
        await conn.run_sync(Base.metadata.create_all)
