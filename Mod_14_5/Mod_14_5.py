from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from CRUD_funcs import get_all_products
from CRUD_funcs import is_existing
from CRUD_funcs import user_insertion

get_all_products()

API = '*your_API_must_be_here*'
botik = Bot(token=API)
dp = Dispatcher(botik, storage=MemoryStorage())

inl_prod_kb = InlineKeyboardMarkup()  # Buy button pressing inline keyboard
bt_inl_prot = InlineKeyboardButton(text='Protein', callback_data='product_buying')
bt_inl_cas = InlineKeyboardButton(text='Casein', callback_data='product_buying')
bt_inl_creat = InlineKeyboardButton(text='Creatine', callback_data='product_buying')
bt_inl_bcaa = InlineKeyboardButton(text='BCAA', callback_data='product_buying')
inl_prod_kb.row(bt_inl_prot, bt_inl_cas, bt_inl_creat, bt_inl_bcaa)

reg_kb = ReplyKeyboardMarkup(resize_keyboard=True)  # After /start sending main keyboard
bt_reg_calc = KeyboardButton(text='Calculate')
bt_reg_info = KeyboardButton(text='Info')
bt_reg_buy = KeyboardButton(text='Buy')
bt_reg_reg = KeyboardButton(text='Sign up')
reg_kb.row(bt_reg_calc, bt_reg_info)
reg_kb.row(bt_reg_buy)
reg_kb.row(bt_reg_reg)


@dp.message_handler(commands=['start'])  # /start command
async def start(msg):
    await msg.answer("Hi! I can calculate your daily calorie limit. "
                     'Take a look at our assortment and stay tuned for updates', reply_markup=reg_kb)


@dp.message_handler(text='Info')  # Info button
async def get_formulas(msg):
    await msg.answer('To calculate your daily limit we use the universal version of Mifflin-San Géor formula: '
                     '\n10 x weight (kg) + 6,25 x height (sm) – 5 x age (yr) – 100')


@dp.message_handler(text='Buy')  # Buy button
async def get_products_list(msg):
    products = get_all_products()
    for product in products:
        title, description, price = product[1], product[2], product[3]  # Unpacking no id tuple

        product_info = (f'Title: {title} | '
                        f'Description: {description} | '
                        f'Price: {price} $')

        image_file = None  # Initializing var

        if title == '№1 Protein':
            image_file = 'pic_protein.jpg'
        elif title == 'Gold Standard Casein':
            image_file = 'pic_casein.jpg'
        elif title == 'GLS Creatine Monohydrate Powder':
            image_file = 'pic_creatine.jpg'
        elif title == 'GLS BCAA Powder':
            image_file = 'pic_bcaa.jpg'

        if image_file:
            with open(image_file, 'rb') as img:
                await msg.answer(product_info)
                await msg.answer_photo(img)
        else:
            await msg.answer(product_info)

        await msg.answer('What would you like to buy?', reply_markup=inl_prod_kb)


@dp.callback_query_handler(text='product_buying')  # Buy button confirmation
async def confirmation_msg(call):
    await call.message.answer('Your purchase has been successfully processed!')


class UserState(StatesGroup):  # Calculation button logic is below
    age = State()
    height = State()
    weight = State()


@dp.message_handler(text='Calculate')
async def set_age(msg):
    await msg.answer('How old are you?')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_height(msg, state):
    await state.update_data(age=msg.text)
    await msg.answer('How tall are you?')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(msg, state):
    await state.update_data(height=msg.text)
    await msg.answer('How much do you weigh?')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(msg, state):
    await state.update_data(weight=msg.text)
    data = await state.get_data()
    age = int(data.get('age', 0))
    height = int(data.get('height', 0))
    weight = int(data.get('weight', 0))
    await msg.answer(f'Your daily calorie limit to start losing weight is: '
                     f'{10 * weight + 6.25 * height - 5 * age - 100} Cal.')
    await state.finish()


class RegistrationState(StatesGroup):  # Registration button logic is below
    username = State()
    email = State()
    age = State()
    balance = State()  # 1000


@dp.message_handler(text='Sign up')
async def sign_up(msg):
    await msg.answer('Enter the user name (Latin alphabet only): ', reply_markup=reg_kb)
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(msg, state):
    username = msg.text

    if is_existing(username):
        await msg.answer('The user already exists, try another name: ')
    else:
        await state.update_data(username=username)
        await msg.answer('Enter your e-mail: ')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(msg, state):
    email = msg.text
    await state.update_data(email=email)
    await msg.answer('Enter your age: ')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(msg, state):
    age = msg.text
    await state.update_data(age=age)

    user_data = await state.get_data()
    username = user_data['username']
    email = user_data['email']
    age = user_data['age']

    user_insertion(username, email, age)

    await msg.answer('Registration completed successfully!', reply_markup=reg_kb)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
