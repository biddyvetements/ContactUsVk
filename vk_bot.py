import asyncio

from vkbottle import Text, Keyboard
from vkbottle.bot import Bot, Message
from keyboards import main_menu_keyboard, cancel_keyboard, confirm_send_keyboard
from states import SendNewsStates
from utils import report_to_admin

# from utils import report_to_admin

bot = Bot(
    token="vk1.a.pFHEFJWwjVYIWnAo5k26wli7_B-OpIWa0x5ZqB13y4xupmEftzBfy99OuQcnSggEkHqS8LD4sgj0jH-Uz7IYqjYGLnr1kRzcQpM_8oJTDVB7WfbapYkYpbNy-i0mi_k2DYSZFSfEBYhDhpbv4owuEaLHoxmKMYD2WhsA6MXvjTSOytN0a3YD8-p9shGPXJ3Ppj6DWGWStcNtMulILwwSTA")


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
        text = '☺️ Спасибо!\n\nНаша команда была проинформирована, ожидайте ответа в ближайшее врем'
    else:
        text = 'Для отправки новости нажмите кнопку ниже 👇🏻'
    await message.answer(message=text, keyboard=main_menu_keyboard.get_json())
    await bot.state_dispenser.delete(message.peer_id)


if __name__ == '__main__':
    asyncio.run(bot.run_polling())
