from vkbottle import BaseStateGroup


class SendNewsStates(BaseStateGroup):
    send_city_name = 'city'
    send_news = 'news'
    send_confirm = 'confirm'
