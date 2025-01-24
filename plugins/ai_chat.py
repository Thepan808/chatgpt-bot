# ©️biisal jai shree krishna 😎
import asyncio
import random
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import FloodWait
from info import *
from plugins.utils import create_image, get_ai_response 
from .db import *
from .fsub import get_fsub


@Client.on_message(filters.command("start") & filters.incoming) # type:ignore
async def startcmd(client: Client, message: Message):
    userMention = message.from_user.mention()
    if await users.get_user(message.from_user.id) is None:
        await users.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#New_user_started\n\nUser: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    if FSUB and not await get_fsub(client, message):return
    await message.reply_photo(# type:ignore
        photo="https://telegra.ph/file/595e38a4d76848c01b110.jpg",
        caption=f"<b>Opa {userMention},\n\nEu poderei te ajudar de seguintes formas..\nUsando-se atráves do privado..\nAsᴋ Mᴇ Aɴʏᴛʜɪɴɢ...Dɪʀᴇᴄᴛʟʏ..\n\nMʏ Cʀᴇᴀᴛᴏʀ : <a href=https://t.me/lndescritivel>Zzz</a>\nMʏ Channel : <a href=t.me/Traps1>Tʜɪs Pᴇʀsᴏɴ</a></b>",
    ) 
    return


@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN)) # type:ignore
async def broadcasting_func(client : Client, message: Message):
    msg = await message.reply_text("Wait a second!") # type:ignore
    if not message.reply_to_message:
        return await msg.edit("<b>Please reply to a message to broadcast.</b>")
    await msg.edit("Processing ...")
    completed = 0
    failed = 0
    to_copy_msg = message.reply_to_message
    users_list = await users.get_all_users()
    for i , userDoc in enumerate(users_list):
        if i % 20 == 0:
            await msg.edit(f"Total : {i} \nCompleted : {completed} \nFailed : {failed}")
        user_id = userDoc.get("user_id")
        if not user_id:
            continue
        try:
            await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ 🎗️", url='https://t.me/lndescritivel')]]))
            completed += 1
        except FloodWait as e:
            if isinstance(e.value , int | float):
                await asyncio.sleep(e.value)
                await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ 🎗️", url='https://t.me/lndescritivel')]]))
                completed += 1
        except Exception as e:
            print("Error in broadcasting:", e) 
            failed += 1
            pass
    await msg.edit(f"Successfully Broadcasted\nTotal : {len(users_list)} \nCompleted : {completed} \nFailed : {failed}")
    

@Client.on_message(filters.command("ai") & filters.chat(CHAT_GROUP)) # type:ignore
async def grp_ai(client: Client, message: Message):
    query : str | None = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    if not query:
        return await message.reply_text( # type:ignore
            "<b>Abe gadhe /ai e ae pai !!.\n\nExemplo Use:\n<code>/ai 7x5??</code>\n\nHope you got it.Try it now..</b>"
        )
    if FSUB and not await get_fsub(client, message):return
    message.text = query # type:ignore
    return await ai_res(client, message)


@Client.on_message(filters.command("reset") &  filters.private) # type:ignore
async def reset(client: Client, message: Message):
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        is_reset = await chat_history.reset_history(message.from_user.id)
        if not is_reset:
            return await message.reply_text("Unable to reset chat history.") # type:ignore
        await message.reply_text("<b>Chat history has been reset.</b>") # type:ignore
    except Exception as e:
        print("Error in reset: ", e)
        return await message.reply_text("Sorry, Failed to reset chat history.") # type:ignore


@Client.on_message(filters.command("gen") & filters.private)  # type:ignore
async def gen_image(client: Client, message: Message):
    """
    Handles private messages with the /gen command and generates an image based on the provided prompt.
    
    Args:
        client (Client): The Client object.
        message (Message): The Message object.

    Returns:
        None
    """
    sticker = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        prompt = message.text.replace("/gen", "").strip()
        encoded_prompt = prompt.replace("\n", " ")
        if not prompt:
            return await message.reply_text("Please provide a prompt.") # type:ignore
        image_file = await create_image(encoded_prompt)
        if not image_file:
            return await message.reply_text("Failed to generate image.") # type:ignore
        await message.reply_photo(photo=image_file , caption=f"Generated Image for prompt: {prompt[:150]}...") # type:ignore
        image_file.close()
    except Exception as e:
        print("Error in gen_image: ", e)
        return await message.reply_text("Sorry, I am not Available right now.") # type:ignore
    finally:
        if sticker:await sticker.delete()

@Client.on_message(filters.text & filters.incoming & filters.private) # type:ignore
async def ai_res(client: Client, message: Message ):
    """
    Handles private text messages and sends AI responses back.
    """
    sticker = None
    reply = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        text = message.text
        if text.startswith('/'):
            return
        user_id = message.from_user.id
        history = await chat_history.get_history(user_id)
        history.append({"role": "user", "content": text})
        reply = await get_ai_response(history)
        history.append({"role": "assistant", "content": reply})
        await message.reply_text(reply) # type:ignore
        await chat_history.add_history(user_id, history)
    except Exception as e:
        print("Error in ai_res: ", e)
        reply = "Sorry, I am not available right now."
        await message.reply_text(reply) # type:ignore
    finally:
        if sticker:
            await sticker.delete()
