import asyncio
from vkbottle import Text, Keyboard
from vkbottle.api import API
from vkbottle.bot import Bot, Message, run_multibot

from config import tokens_list
from keyboards import main_menu_keyboard, cancel_keyboard, confirm_send_keyboard
from states import SendNewsStates, AnswerAdmins
from utils import report_to_admin
import logging

bot = Bot()
api = API(
    token='vk1.a.6cvd9dS71kARWykfdxDm5cDT9sPIASHqeS0Uij44Mjn08PKdom9nuHd1su9oiAmzW1YW9XZtQX4UJ90djoG82kJY66Ph-cs4ucl-alS2vwo-ikAkayT4ZVU9D8Jr5ulXWuX5OOYNWzwstxelXOW7nb4zmg53A8GoRzjlJoDZQKYrV0M_y2o71fjZxatRSkKSgkvjHgR2DUS1q-yTtfGZhA')


# rSyjLkdpM8mSYRQpxCZE



@bot.on.message(text='❌ Отмена')
async def main_menu(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    text = 'Для отправки новости нажмите кнопку ниже 👇🏻'
    await message.answer(message=text, keyboard=main_menu_keyboard.get_json())


@bot.on.message(text="Начать")
async def main_menu_handler(message: Message):
    text = 'Для отправки новости нажмите кнопку ниже 👇🏻'
    await message.answer(message=text, keyboard=main_menu_keyboard.get_json())


@bot.on.message(text='✍️ Сообщить о происшествии')
async def begin_news_report(message: Message):
    text = 'В следующем сообщении кратко изложите суть новости.'
    await bot.state_dispenser.set(message.peer_id, SendNewsStates.send_news)
    await message.answer(message=text, keyboard=cancel_keyboard.get_json())


@bot.on.message(state=SendNewsStates.send_news)
async def fetch_news_text(message: Message):
    text = ('Пожалуйста, проверьте введенную вами новость:\n\n'
            f'{message.text}')
    await bot.state_dispenser.set(message.peer_id, SendNewsStates.send_confirm, news_text=message.text)
    await message.answer(message=text, keyboard=confirm_send_keyboard)


@bot.on.message(state=SendNewsStates.send_confirm)
async def confirm_answer(message: Message):
    if message.text == '✅ Отправить':
        group = await api.groups.get_by_id(message.group_id)
        state_data = await bot.state_dispenser.get(message.peer_id)
        state_data = state_data.payload
        text_to_admin = f"Сообщили o новости в *{group[0].name}*\n\n{state_data['news_text']} \n\nОт пользователя https://vk.com/id{message.peer_id}"
        await report_to_admin(text_to_admin, message.peer_id, message.group_id)
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
    logging.getLogger("vkbottle").setLevel(logging.INFO)
    run_multibot(bot, apis=(API(i) for i in tokens_list))

# kazan vk1.a.w2RUNqNEtVMtBGtyylOP_IXaGs95iwem3qXhJL_nxk6-sxhJ4RKLpWJ9OY81qXuX7QehUr0oGK9NZJyXrgDia6EDLGRNl5GV2yYooD5LpJ43VbC52bUyE3mS9ayyn0kD00G-9R0RT5JONVeTi7Ho0ELvb90GIXWeDsSlmuFMNDmxowi9avtCZF8qGpvZdEe4LE2Gr15hsSqbRUh5WCEhtg
