from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from bot.database.requests import set_user, del_tasks, set_tasks
import bot.keyboards as kb

user = Router()


@user.message(CommandStart())
async def start_command(message: Message):
    """Обработчик команды /start."""
    # Создаем пользователя в БД
    await set_user(message.from_user.id)
    await message.answer(
        'Нажмите на выполненную задачу, чтобы удалить '
        'или напишите в чат новую.',
        reply_markup=await kb.tasks(message.from_user.id)
    )


@user.callback_query(F.data.startswith('task_'))
async def delete_task(callback: CallbackQuery):
    """Обработчик удаления задачи."""
    # Отправляем уведомление
    await callback.answer('Задача выполнена!')
    # Удаляем задачу из БД
    await del_tasks(callback.data.split('_')[1])
    # Удаляем сообщение с задачей
    await callback.message.delete()
    await callback.message.answer(
        'Нажмите на выполненную задачу, чтобы удалить '
        'или напишите в чат новую.',
        reply_markup=await kb.tasks(callback.from_user.id)
    )


@user.message()
async def add_task(message: Message):
    """Обработчик добавления задачи."""
    # Если длина задачи больше 100 символов
    if len(message.text) > 100:
        # Уведомляем
        await message.answer(
            '❌ <b>Задача слишком длинная.</b>\n\n'
            'Количество символов превышает 100 знаков. '
            'Попробуй еще.'
        )
        return
    # Добавляем задачу в БД
    await set_tasks(message.from_user.id, message.text)
    await message.answer(
        '✅ <b>Задача добавлена!</b>\n\nНажмите на выполненную задачу,'
        ' чтобы удалить или напишите в чат новую.',
        reply_markup=await kb.tasks(message.from_user.id)
    )
