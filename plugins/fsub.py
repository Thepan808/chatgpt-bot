from typing import List
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton , InlineKeyboardButtonBuy
from pyrogram.types import Message
from pyrogram.client import Client
from info import *

async def get_fsub(bot : Client, message: Message ) -> bool:
    """
    Verifica se o usuário é assinante do canal e, se não for, pede para ele entrar no canal.

    Parâmetros:
    bot (Client): A instância do cliente.
    message (Message): A mensagem que disparou a função.

    Retorna:
    bool: True se o usuário for assinante, False caso contrário.
    """
    target_channel_id = AUTH_CHANNEL  # ID do seu canal
    user_id = message.from_user.id
    try:
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        channel_link :str  = (await bot.get_chat(target_channel_id)).invite_link #type: ignore
        join_button = InlineKeyboardButton("Entrar no Canal", url=channel_link) # type:ignore
        keyboard : List[List[InlineKeyboardButton | InlineKeyboardButtonBuy]] = [[join_button]]
        await message.reply( # type:ignore
            f"<b>Caro usuário {message.from_user.mention}!\n\nPor favor, entre no nosso canal de atualizações para me usar! 😊\n\nDevido ao servidor...</b>",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    return True
