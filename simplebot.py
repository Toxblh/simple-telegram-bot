"""
Simple bot for managing local chat
"""
import random
import os
import re
from typing import Union
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.builtin import IDFilter

WELCOME_TEXT = """Приветствуем тебя в Linux Sucks, <b>{}</b>!
Мы здесь чтобы спорить о *nix системах, делиться опытом, просто общаться и иногда решать проблемы и помогать друг другу. Присоединяйся и развивайся с нами!"""
RULES_TEXT = """<b>Правила LinuxSucks</b>
0. Чат создан не для техподдержки, а прежде всего для уважительного общения.
1. Относитесь друг к другу уважительно.
2. Мат разрешен, но не в оскорбительном тоне.
3. Любой спор не должен перетекать в оскорбления и/или троллинг.
4. Избегайте размещения nsfw контента (https://ru.wikipedia.org/wiki/NSFW).
5. Любой спам / флуд / шитпостинг запрещены.
6. Любые проявления нетерпимости ставят вас под угрозу бана, имейте это ввиду.
Вопросы задавать можно, но стоит научиться делать это правильно - https://nometa.xyz/"""

project_folder = os.path.expanduser('./')  
load_dotenv(os.path.join(project_folder, '.env'))

CHAT_ID = os.getenv("CHATID")
TOKEN = str(os.getenv("TOKEN"))

bot = Bot(token=TOKEN,
          parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(
    IDFilter(chat_id=CHAT_ID),  # Add chat_id filter to handlers since we
                                # don't need to handle all chats bot added
    #commands=['start'])
    content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def welcome(message: types.Message):
    """
    Handles new members joining the chat
    """
    if message.from_user not in message.new_chat_members:
        # Skip members added by someone assuming they were explained the rules
        return
    with open("id.txt") as f:
            sticker = random.choice(list(f.readlines()))
            sticker = sticker.rstrip()
    await bot.send_sticker(message.chat.id, sticker, 'rb') 

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Правила", callback_data='rules')
    markup.add(item1)

    # Assuming only one member has joined at the same time
    new_member = message.new_chat_members[0]

    await message.reply(WELCOME_TEXT.format(new_member.username), reply_markup=markup, reply=False)

@dp.callback_query_handler(IDFilter(chat_id=CHAT_ID), text="rules")
@dp.message_handler(IDFilter(chat_id=CHAT_ID), commands=['rules'])
async def rules(update: Union[types.CallbackQuery, types.Message]):
    """
    shows the chat rules
    """
    message = update
    # if we're handling the callback query, we have message in .message:
    if isinstance(update, types.CallbackQuery):
        message = update.message

    await bot.send_message(message.chat.id, RULES_TEXT)
    if isinstance(update, types.Message):
        return
    await update.answer()
    await update.message.delete_reply_markup()

@dp.message_handler(lambda message: message.text.lower() )
async def echo_message(message: types.Message):

    wordsban = ["бан", "ban", ",fy", "<fy", "тебе бан"]
    wordlin = ["лялих", "лялех", "люнекс", "линекс"]
    word_blin = ["Блина", "блина", "ну блина"]

    array =  message.text.split(" ")
    for el in array:
        if el in wordsban:
            return await message.reply("Жан Клод Вам Бан")
        if el in wordlin:
            return await message.reply("— Hello, this is Linus Torvalds, and I pronounce Linux as [ˈlɪnʊks].")
        if el in word_blin:
            return await message.reply("«Индекс блина» в России за год снизился на 9%")

if __name__ == '__main__':    
    executor.start_polling(dp, skip_updates=True)
