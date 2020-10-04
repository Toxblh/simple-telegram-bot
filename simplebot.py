"""
Simple bot for managing local chat
"""
import random
import os
from typing import Union

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.builtin import IDFilter

CHAT_ID = -chat_id
TOKEN = "TO:KEN"

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


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
