from vkbottle import Keyboard, Text, KeyboardButtonColor

main_menu_keyboard = Keyboard(inline=True)
main_menu_keyboard.add(Text("✍️ Сообщить о происшествии"))

cancel_keyboard = Keyboard(inline=True)
cancel_keyboard.add(Text('❌ Отмена'), color=KeyboardButtonColor.NEGATIVE)

confirm_send_keyboard = Keyboard(inline=True)
confirm_send_keyboard.add(Text('✅ Отправить'), color=KeyboardButtonColor.POSITIVE)
confirm_send_keyboard.add(Text('❌ Отмена'), color=KeyboardButtonColor.NEGATIVE)
