import asyncio
from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound

from config import admins_list, tokens_list
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode


async def report_to_admin(news_text: str, sender_id: int, group_id: int):
    TOKEN = '6410038704:AAHPMNYx-AuLvfwSCzD26GQk-sLmXg7LlDw'
    tg_bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
    for admin in admins_list:
        answer_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(callback_data=f'answer_user_vk_{sender_id}_{group_id}', text='📢 Ответить')]])
        try:
            await tg_bot.send_message(chat_id=admin, text=news_text)
                                      #, reply_markup=answer_inline_keyboard)
        except ChatNotFound:
            pass
