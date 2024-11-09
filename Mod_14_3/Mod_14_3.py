from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API = '*your_API_must_be_here*'
botik = Bot(token=API)
dp = Dispatcher(botik, storage=MemoryStorage())

#  Products description is below
it_1_title = '№1 Protein'
it_1_description = 'High-quality protein powder to support muscle growth and recovery'
it_2_title = 'Gold Standard Casein'
it_2_description = 'Slow-digesting protein for sustained muscle support during sleep'
it_3_title = 'GLS Creatine Monohydrate Powder'
it_3_description = 'Boosts muscle strength and power, enhancing workout performance'
it_4_title = 'GLS BCAA Powder'
it_4_description = 'Branched-chain amino acids for muscle repair and reduced fatigue'
price_multiplier_num = 4.20

it_1 = (f'Title: {it_1_title} | '
        f'Description: {it_1_description} | '
        f'Price: {round(price_multiplier_num * 4.2, 2)} $')

it_2 = (f'Title: {it_2_title} | '
        f'Description: {it_2_description} | '
        f'Price: {round(price_multiplier_num * 5.1, 2)} $')

it_3 = (f'Title: {it_3_title} | '
        f'Description: {it_3_description} | '
        f'Price: {round(price_multiplier_num * 3.5, 2)} $')

it_4 = (f'Title: {it_4_title} | '
        f'Description: {it_4_description} | '
        f'Price: {round(price_multiplier_num * 3.2, 2)} $')

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
reg_kb.row(bt_reg_calc, bt_reg_info)
reg_kb.row(bt_reg_buy)


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
    with open('pic_protein.jpg', 'rb') as img_prot:
        await msg.answer(it_1)
        await msg.answer_photo(img_prot)
    with open('pic_casein.jpg', 'rb') as img_cas:
        await msg.answer(it_2)
        await msg.answer_photo(img_cas)
    with open('pic_creatine.jpg', 'rb') as img_creat:
        await msg.answer(it_3)
        await msg.answer_photo(img_creat)
    with open('pic_bcaa.jpg', 'rb') as img_bcaa:
        await msg.answer(it_4)
        await msg.answer_photo(img_bcaa)
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
