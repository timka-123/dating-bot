from os import environ

from aiogram import Router, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile, CallbackQuery
from aiohttp import ClientSession
from dotenv import load_dotenv

from database import get_user, update_user_info
from keyboards.profile_kb import profile_kb
from states import UserStates

router = Router()


@router.message(Text("👤 Профиль"))
async def profile(message: Message):
    user = get_user(message.from_user.id)
    await message.answer_photo(
        photo=URLInputFile(user.photo_link),
        caption=f"""<b>ℹ️ Информация о вас</b>

👤 Имя: {user.name}
📍 Город: {user.city}
👍 Возраст: {user.age}
📃 О вас: {user.about}""",
        reply_markup=profile_kb()
    )


@router.callback_query(lambda c: c.data.startswith("change_"))
async def change_data(call: CallbackQuery, state: FSMContext):
    cmd, action = call.data.split('_')
    await state.update_data(action=action)
    await state.set_state(UserStates.UPDATE_DATA)
    await call.message.delete()
    await call.message.answer("<b>✏️ Введите новые данные</b>")


@router.message(UserStates.UPDATE_DATA)
async def update_data(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    value = message.text
    if data['action'] == "photo":
        load_dotenv()
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, "image.jpg")
        img_data = b""
        with open("image.jpg", "rb") as file:
            img_data += file.read()
        async with ClientSession(headers={
            "Content-Type": "image/jpeg"
        }) as session:
            response = await session.post(
                url=f"https://www.filestackapi.com/api/store/S3?key={environ.get('FILESTACK_API_KEY')}",
                data=open("image.jpg", "rb")
            )
            rdata = await response.json()
            await session.close()
        value = rdata['url']
    update_user_info(message.from_user.id, data['action'], value)
    user = get_user(message.from_user.id)
    await message.answer_photo(
        photo=URLInputFile(user.photo_link),
        caption=f"""<b>ℹ️ Информация о вас</b>

👤 Имя: {user.name}
📍 Город: {user.city}
👍 Возраст: {user.age}
📃 О вас: {user.about}""",
        reply_markup=profile_kb()
    )
