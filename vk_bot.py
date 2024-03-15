import asyncio

from vkbottle import Text, Keyboard
from vkbottle.bot import Bot, Message
from keyboards import main_menu_keyboard, cancel_keyboard, confirm_send_keyboard
from states import SendNewsStates, AnswerAdmins
from utils import report_to_admin

# from utils import report_to_admin

bot = Bot(
    token="vk1.a.AX7lLnQwWk7BfMsTgLzRwH9iGaRC6t6SantgWnkdz1DFSWHmCigGYONN-os6fKfA5FxNjh4AnafLH1Gg0Fi01JU95Hop2bZ2qjad2xCVSl7rDxvkGQV8kODnHfGAOrmZyanyNf7tbrTyZwSHVWAkRb1LVkmvO4ymYK3ab7qbLDyS0tNkMeBdcDCquzAhkuTwgZ6Fsu2dD-pghckzAVxagA")
# cancel_keyboard

@bot.on.message(text="Начать")
async def main_menu_handler(message: Message):
    text = 'Для отправки новости нажмите кнопку ниже 👇🏻'
    await message.answer(message=text, keyboard=main_menu_keyboard.get_json())


@bot.on.message(text='✍️ Сообщить о происшествии')
async def begin_news_report(message: Message):
    text = 'В следующем сообщении отправьте название города в котором произошла новость.'
    await bot.state_dispenser.set(message.peer_id, SendNewsStates.send_city_name)
    await message.answer(message=text, keyboard=cancel_keyboard.get_json())


@bot.on.message(state=SendNewsStates.send_city_name)
async def fetch_city_name(message: Message):
    text = 'Отлично 👍\n\nВ следуюшем сообщении изложите суть новости'
    await bot.state_dispenser.set(message.peer_id, SendNewsStates.send_news, city_name=message.text)
    await message.answer(message=text, keyboard=cancel_keyboard.get_json())


@bot.on.message(state=SendNewsStates.send_news)
async def fetch_news_text(message: Message):
    state_data = await bot.state_dispenser.get(message.peer_id)
    state_data = state_data.payload
    text = ('Пожалуйста, проверьте введенную вами новость:\n\n'
            f'{state_data["city_name"]}\n'
            f'{message.text}')
    await bot.state_dispenser.set(message.peer_id, SendNewsStates.send_confirm, news_text=message.text,
                                  city_name=state_data['city_name'])
    await message.answer(message=text, keyboard=confirm_send_keyboard)


@bot.on.message(state=SendNewsStates.send_confirm)
async def confirm_answer(message: Message):
    if message.text == '✅ Отправить':
        state_data = await bot.state_dispenser.get(message.peer_id)
        state_data = state_data.payload
        text_to_admin = f"Сообщили o новости в городе *{state_data['city_name']}* в Вконтакте\n\n{state_data['news_text']} \n\nОт пользователя https://vk.com/id{message.peer_id}"
        await report_to_admin(text_to_admin, message.peer_id)
        text = '☺️ Спасибо!\n\nНаша команда была проинформирована, ожидайте ответа в ближайшее время'
    else:
        text = 'Для отправки новости нажмите кнопку ниже 👇🏻'
    await message.answer(message=text, keyboard=main_menu_keyboard.get_json())
    await bot.state_dispenser.delete(message.peer_id)


@bot.on.message(text='💬 Ответить')
async def answer_to_admin(message: Message):
    await bot.state_dispenser.set(message.peer_id, AnswerAdmins.send_answer_text)
    await message.answer(message='Введите текст для ответа в следующем  сообщении')


@bot.on.message(state=AnswerAdmins.send_answer_text)
async def answer_to_admin(message: Message):
    text = '☺️ Спасибо!\n\nНаша команда была проинформирована, ожидайте ответа в ближайшее время'
    await report_to_admin(f'Получено сообщение по обращению:\n\n{message.text}', message.peer_id)
    await message.answer(message=text, keyboard=main_menu_keyboard.get_json())
    await bot.state_dispenser.delete(message.peer_id)


if __name__ == '__main__':
    asyncio.run(bot.run_polling())
