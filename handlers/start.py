from os import environ

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession

from keyboards.reg_kbs import name_kb, city_kb
from keyboards.menu_kb import menu_kb
from states import UserStates
from database import create_user, get_user
from dotenv import load_dotenv

router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if user:
        return await message.answer("Добро пожаловать!",
                                    reply_markup=menu_kb())
    await message.answer("Добро пожаловать! Введите Ваше имя",
                         reply_markup=name_kb(message.from_user.first_name))
    await state.set_state(UserStates.ENTER_NAME)


@router.message(UserStates.ENTER_NAME)
async def enter_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите Ваш возраст!")
    await state.set_state(UserStates.ENTER_AGE)


@router.message(UserStates.ENTER_AGE, lambda m: m.text.isdigit())
async def enter_city(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Отправьте свое местоположение для определения города",
                         reply_markup=city_kb())
    await state.set_state(UserStates.ENTER_CITY)


@router.message(UserStates.ENTER_CITY)
async def enter_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(UserStates.ENTER_INFO)
    await message.answer("Расскажи что-нибудь о себе!")


@router.message(UserStates.ENTER_INFO)
async def upload_photo(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, пришли свою фотографию")
    await state.update_data(about=message.text)
    await state.set_state(UserStates.UPLOAD_PHOTO)


@router.message(UserStates.UPLOAD_PHOTO, lambda m: True if m.photo else False)
async def accept_data(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()
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
    image_link = rdata['url']
    create_user(
        user_id=message.from_user.id,
        name=data['name'],
        about=data['about'],
        photo_link=image_link,
        age=data['age'],
        city=data['city']
    )
    await message.answer("Успешно! Анкета добавлена в поиск!", reply_markup=menu_kb())

