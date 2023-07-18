from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext

from states import UserStates
from database import get_user, get_users
from keyboards.search_kb import user_actions, reply_actions

router = Router()


@router.message(Text("🚀 Искать"))
async def search(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    users = get_users(user.city, message.from_user.id)
    if not users:
        return await message.answer("😔 Нет пользователей в вашем городе...")
    await state.set_state(UserStates.SEARCH_PEOPLE)
    await state.update_data(
        city=user.city,
        index=1,
        users=users
    )
    current_user = users[0]
    await message.answer_photo(
        caption=f"👤 Имя: {current_user.name}\n👍 Возраст: {current_user.age} лет\n📍 Город: {current_user.city}\n📄 О себе: {current_user.about}",
        reply_markup=user_actions(current_user.id),
        photo=URLInputFile(current_user.photo_link)
    )


@router.callback_query(UserStates.SEARCH_PEOPLE, lambda c: c.data.startswith("like_"))
async def like_user(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    cmd, user_id = call.data.split('_')
    current_user = get_user(call.from_user.id)
    await bot.send_message(
        chat_id=user_id,
        text=f"""👍 Вы понравились пользователю!

👤 Имя: {current_user.name}
👍 Возраст: {current_user.age} лет
📍 Город: {current_user.city}
📄 О себе: {current_user.about}
""",
        reply_markup=reply_actions(current_user.id)
    )
    users = get_users(current_user.city, call.from_user.id)
    try:
        current_user = users[data['index']]
    except:
        await call.answer("✅ Вы просмотрели всех пользователей")
        await call.message.delete()
        await state.clear()
        return
    await call.message.delete()
    await call.message.answer_photo(
        caption=f"👤 Имя: {current_user.name}\n👍 Возраст: {current_user.age} лет\n📍 Город: {current_user.city}\n📄 О себе: {current_user.about}",
        reply_markup=user_actions(current_user.id),
        photo=URLInputFile(current_user.photo_link)
    )
    await state.update_data(index=data['index'] + 1)
    await call.answer("👍 Отправлено")


@router.callback_query(UserStates.SEARCH_PEOPLE, lambda c: c.data.startswith("dislike_"))
async def dislike_user(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    current_user = get_user(call.from_user.id)
    users = get_users(current_user.city, call.from_user.id)
    try:
        current_user = users[data['index']]
    except:
        await call.answer("✅ Вы просмотрели всех пользователей")
        await call.message.delete()
        await state.clear()
        return
    await call.message.delete()
    await call.message.answer_photo(
        caption=f"👤 Имя: {current_user.name}\n👍 Возраст: {current_user.age} лет\n📍 Город: {current_user.city}\n📄 О себе: {current_user.about}",
        reply_markup=user_actions(current_user.id),
        photo=URLInputFile(current_user.photo_link)
    )
    await state.update_data(index=data['index'] + 1)
    await call.answer("👍 Отправлено")


@router.callback_query(UserStates.SEARCH_PEOPLE, Text("stop"))
async def stop_searching(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer("Главное меню")


@router.callback_query(lambda c: c.data.startswith("ans_"))
async def action_answer(call: CallbackQuery, bot: Bot):
    cmd, action, user_id = call.data.split('_')
    user = get_user(user_id)
    if action == "like":
        await call.message.reply(
            text=f'<b>Хорошо провести вам время: <a href="tg://user?id={user_id}">{user.name}</a></b>'
        )
        await bot.send_message(
            chat_id=user_id,
            text=f'<b>Хорошо провести вам время: <a href="tg://user?id={call.from_user.id}">{call.from_user.first_name}</a></b>'
        )
        await call.message.edit_text(
            text=call.message.html_text,
            reply_markup=None
        )
    elif action == "dislike":
        await call.message.delete()
