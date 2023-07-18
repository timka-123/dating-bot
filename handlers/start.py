from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reg_kbs import name_kb, city_kb
from keyboards.menu_kb import menu_kb
from states import UserStates
from database import create_user, get_user

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
async def enter_city(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    data = await state.get_data()
    create_user(user_id=message.from_user.id, name=data['name'],
                about=data['info'], age=data['age'], city=data['city'])
    await state.clear()
    await message.answer("Спасибо! Твоя анкета теперь в поиске",
                         reply_markup=menu_kb())
