from aiogram.types import (
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.requests import get_tasks


async def tasks(telegram_id: int):
    """Возвращает клавиатуру c задачами."""
    # Собираем таски из БД
    tasks = await get_tasks(telegram_id)
    # Создаем клавиатуру
    keyboard = InlineKeyboardBuilder()
    # Добавляем кнопки с задачами
    for task in tasks:
        keyboard.add(InlineKeyboardButton(
            text=task.task,
            callback_data=f'task_{task.id}'
        ))
    return keyboard.adjust(1).as_markup()
