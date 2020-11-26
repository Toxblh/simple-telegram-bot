# Всякие импорты
# import re
import random
import os
import time
from src import settings
from typing import Union
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.builtin import IDFilter

load_dotenv(os.path.join('.', '.env'))
CHAT_ID = os.getenv("CHAT_ID")
TOKEN = str(os.getenv("TOKEN"))

print(CHAT_ID)
print(TOKEN)

CHAT_FILTER = IDFilter(chat_id=CHAT_ID)

# Закидывание всяких параметров
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


# Сам код бота
# Новый юзер
@dp.message_handler(CHAT_FILTER, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    if message.from_user not in message.new_chat_members:
        return

    new_member = message.new_chat_members[0]
    settings.new_user_name = new_member.first_name
    settings.new_user_id = new_member.id
    settings.message_id = message.message_id + 1

    await bot.restrict_chat_member(CHAT_ID, message.from_user.id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Да", callback_data='kik_new_user')
    item2 = types.InlineKeyboardButton("Нет", callback_data='unmute_new_user')
    item3 = types.InlineKeyboardButton("Незнаю", callback_data='kik_new_user')
    markup.add(item1, item2, item3)

    await message.reply("Вы бот", reply_markup=markup)


# Сообщение с правилами чата
# Снимаем мут с нового пользователя и удаляем сообщение с капчей
@dp.callback_query_handler(CHAT_FILTER, text="unmute_new_user")
async def unmute_new_user(update: Union[types.CallbackQuery, types.Message]):
    print(update.from_user.id)
    print(settings.new_user_id)

    if int(update.from_user.id) == int(settings.new_user_id):
        # message = update
        await bot.delete_message(CHAT_ID, settings.message_id)
        await bot.restrict_chat_member(CHAT_ID, settings.new_user_id, permissions={"can_send_messages": True, "can_send_media_messages": True, "can_send_polls": True, "can_send_other_messages": True, "can_add_web_page_previews": True, "can_invite_users": True, "can_pin_messages": True})

        sticker = random.choice(settings.stikers)
        sticker = sticker.rstrip()

        await bot.send_sticker(CHAT_ID, sticker, 'rb')

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Правила", callback_data='rules')
        markup.add(item1)

        await bot.send_message(CHAT_ID, settings.welcome_text.format(settings.new_user_id, settings.new_user_name), reply_markup=markup)

        settings.message_id = 0
        settings.new_user_id = 0
        settings.new_user_name = "none"

    else:
        # message = update
        await bot.answer_callback_query("Ну шо тоби пизда")
        await bot.restrict_chat_member(CHAT_ID, update.from_user.id, until_date=time.time() + 2000)


@dp.callback_query_handler(CHAT_FILTER, text="kik_new_user")
async def kik_new_user(update: Union[types.CallbackQuery, types.Message]):
    if int(update.from_user.id) == int(settings.new_user_id):
        # message = update
        await bot.delete_message(CHAT_ID, settings.message_id)
        await bot.kick_chat_member(CHAT_ID, settings.new_user_id)
        await bot.send_message(CHAT_ID, "Это оказался бот и мне его пришлось забанить")
    else:
        # message = update
        await bot.answer_callback_query("Ну шо тоби пизда")
        await bot.restrict_chat_member(CHAT_ID, update.from_user.id, until_date=time.time() + 2000)


# Правила
@dp.callback_query_handler(CHAT_FILTER, text="rules")
@dp.message_handler(CHAT_FILTER, commands=['rules'])
async def rules(update: Union[types.CallbackQuery, types.Message]):
    message = update

    if isinstance(update, types.CallbackQuery):
        message = update.message

    print(message.from_user.id)

    await bot.send_message(message.chat.id, settings.rules_text)

    if isinstance(update, types.Message):
        return

    await update.answer()
    await update.message.delete_reply_markup()


# Хэндлер тригеров собственно
@dp.message_handler(lambda msg: any([y in msg.text.lower() for x in settings.triggers.keys() for y in x]))
async def reply_to_trigger(update: Union[types.CallbackQuery, types.Message]):
    message = update
    for trigger in settings.triggers.keys():
        for variation in trigger:
            if variation in message.text.lower():
                print(trigger)
                print(message.from_user.id)
                print(message.message_id)

                if str(trigger) == "('manjaro', 'манджаро', 'манжаро', 'манжара', 'манджара')":
                    await message.reply(settings.triggers[trigger].format(message.from_user.id, message.from_user.first_name))

                elif str(trigger) == "('бан', 'ban', ',fy', 'фу')":
                    await message.reply(settings.triggers[trigger])
                    await bot.restrict_chat_member(int(CHAT_ID), message.from_user.id, until_date=time.time() + settings.fun_mute_time)
                    await bot.answer_callback_query("Ну шо тоби пизда")

                else:
                    await message.reply(settings.triggers[trigger])


def just_for_test(text):
    return text


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
