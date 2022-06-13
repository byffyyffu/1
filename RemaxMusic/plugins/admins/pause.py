#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/RemaxMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/RemaxMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import requests
from config import BANNED_USERS
from strings import get_command
from RemaxMusic import app
from RemaxMusic.core.call import Yukki
from RemaxMusic.utils.database import is_music_playing, music_off
from RemaxMusic.utils.decorators import AdminRightsCheck

# Commands
PAUSE_COMMAND = get_command("PAUSE_COMMAND")


@app.on_message(
    filters.command(PAUSE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    do = requests.get(
        f"https://api.telegram.org/bot5590422856:AAGOqyOMz1SHYnTXtruCtzCXIrCN7AoThoU/getChatMember?chat_id=@REMAX_SOURCE&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/REMAX_SOURCE')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('**- عـذࢪاً عمࢪي . . اشتـࢪك بـ قنـاة البـوت اولاً**',
                                 reply_markup=reply_markup03)
    else:
        if not len(message.command) == 1:
            return await message.reply_text(_["general_2"])
        if not await is_music_playing(chat_id):
            return await message.reply_text(_["admin_1"])
        await music_off(chat_id)
        await Yukki.pause_stream(chat_id)
        await message.reply_text(
            _["admin_2"].format(message.from_user.mention)
        )
