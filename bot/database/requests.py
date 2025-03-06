from sqlalchemy import select, delete

from bot.database.models import async_session
from bot.database.models import User, Task


async def set_user(telegram_id: int):
    """Добавляет пользователя в БД, если его там нет."""
    # Открываем сессию
    async with async_session() as session:

        # Находим пользователя по айди
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

        # Если пользователя нет в БД
        if not user:
            # Добавляем его
            session.add(User(telegram_id=telegram_id))
            # Фиксируем изменения
            await session.commit()


async def get_tasks(telegram_id: int):
    """Получает список задач пользователя."""
    # Открываем сессию
    async with async_session() as session:

        # Находим пользователя по айди
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

        # Получаем все задачи пользователя
        tasks = await session.scalars(
            select(Task).where(Task.user == user.id)
        )
        return tasks


async def set_tasks(telegram_id: int, task):
    """Добавляет задачу пользователя."""
    # Открываем сессию
    async with async_session() as session:

        # Находим пользователя по айди
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

        # Добавляем задачу
        session.add(Task(task=task, user=user.id))
        await session.commit()


async def del_tasks(task_id):
    """Удаляет задачу пользователя."""
    # Открываем сессию
    async with async_session() as session:
        # Удаляем задачу
        await session.execute(
            delete(Task).where(Task.id == task_id)
        )
        await session.commit()
