# ©️biisal jai shree krishna 😎
import asyncio
import random
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from uuid import uuid4
from googletrans import Translator
import requests
from requests.exceptions import HTTPError
from info import *
from plugins.utils import create_image, get_ai_response 
from .db import *
from .fsub import get_fsub

translator = Translator()

async def traduzir_para_portugues(texto):
    return (await translator.translate(texto, dest='pt')).text

@Client.on_message(filters.command("start") & filters.incoming) # type:ignore
async def startcmd(client: Client, message: Message):
    userMention = message.from_user.mention()
    if await users.get_user(message.from_user.id) is None:
        await users.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#Novo_usuario_iniciou\n\nUsuário: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    if FSUB and not await get_fsub(client, message): return
    await message.reply( # type:ignore
        text=f"Opa {userMention},\n\nEu sou um bot de IA. Pergunte-me qualquer coisa.\n\n"
             "Aqui está um resumo dos comandos disponíveis:\n"
             "- /ai <texto>: Pergunte qualquer coisa para a IA.\n"
             "- /gen <prompt>: Gere uma imagem com base no prompt fornecido.\n"
             "- /reset: Redefina o histórico de chat.\n"
             "\nClique no botão abaixo para ver todos os comandos e suas funções.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("DEV", url="https://t.me/lndescritivel")]
            ]
        )
    )
    return

@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN)) # type:ignore
async def broadcasting_func(client: Client, message: Message):
    msg = await message.reply_text("Espere um segundo!") # type:ignore
    if not message.reply_to_message:
        return await msg.edit("<b>Por favor, responda a uma mensagem para transmitir.</b>")
    await msg.edit("Processando ...")
    completed = 0
    failed = 0
    to_copy_msg = message.reply_to_message
    users_list = await users.get_all_users()
    for i, userDoc in enumerate(users_list):
        if i % 20 == 0:
            await msg.edit(f"Total: {i} \nConcluído: {completed} \nFalhou: {failed}")
        user_id = userDoc.get("user_id")
        if not user_id:
            continue
        try:
            await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 Suporte Admin 🎗️", url='https://t.me/lndescritivel')]]))
            completed += 1
        except FloodWait as e:
            if isinstance(e.value , int | float):
                await asyncio.sleep(e.value)
                await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭 Suporte Admin 🎗️", url='https://t.me/lndescritivel')]]))
                completed += 1
        except Exception as e:
            print("Erro na transmissão:", e) 
            failed += 1
            pass
    await msg.edit(f"Transmissão bem-sucedida\nTotal: {len(users_list)} \nConcluído: {completed} \nFalhou: {failed}")

@Client.on_message(filters.command("ai") & filters.chat(CHAT_GROUP)) # type:ignore
async def grp_ai(client: Client, message: Message):
    query: str | None = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    if not query:
        return await message.reply_text( # type:ignore
            "<b>Abe gadhe /ai e ae pai !!.\n\nExemplo de uso:\n<code>/ai 7x5??</code>\n\nEspero que tenha entendido. Tente agora..</b>"
        )
    if FSUB and not await get_fsub(client, message): return
    message.text = query # type:ignore
    return await ai_res(client, message)

@Client.on_message(filters.command("reset") & filters.private) # type:ignore
async def reset(client: Client, message: Message):
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message): return
        is_reset = await chat_history.reset_history(message.from_user.id)
        if not is_reset:
            return await message.reply_text("Não foi possível redefinir o histórico de chat.") # type:ignore
        await message.reply_text("<b>O histórico de chat foi redefinido.</b>") # type:ignore
    except Exception as e:
        print("Erro na redefinição: ", e)
        return await message.reply_text("Desculpe, falha ao redefinir o histórico de chat.") # type:ignore

@Client.on_message(filters.command("gen") & filters.private)  # type:ignore
async def gen_image(client: Client, message: Message):
    """
    Lida com mensagens privadas com o comando /gen e gera uma imagem com base no prompt fornecido.
    
    Args:
        client (Client): O objeto Client.
        message (Message): O objeto Message.

    Returns:
        None
    """
    sticker = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message): return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        prompt = message.text.replace("/gen", "").strip()
        encoded_prompt = prompt.replace("\n", " ")
        if not prompt:
            return await message.reply_text("Por favor, forneça um prompt.") # type:ignore
        try:
            image_file = await create_image(encoded_prompt)
            if not image_file:
                return await message.reply_text("Falha ao gerar a imagem.") # type:ignore
            await message.reply_photo(photo=image_file, caption=f"Imagem gerada para o prompt: {prompt[:150]}...") # type:ignore
            image_file.close()
        except HTTPError as http_err:
            await message.reply_text(f"HTTP error occurred: {http_err}")
        except Exception as err:
            await message.reply_text(f"Other error occurred: {err}")
    except Exception as e:
        print("Erro ao gerar imagem: ", e)
        return await message.reply_text("Desculpe, não estou disponível no momento.") # type:ignore
    finally:
        if sticker: await sticker.delete()

@Client.on_message(filters.text & filters.incoming & filters.private) # type:ignore
async def ai_res(client: Client, message: Message):
    """
    Lida com mensagens de texto privadas e envia respostas de IA de volta.
    """
    sticker = None
    reply = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message): return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        text = message.text
        if text.startswith('/'):
            return
        user_id = message.from_user.id
        history = await chat_history.get_history(user_id)
        history.append({"role": "user", "content": text})
        reply = await get_ai_response(history)
        reply = await traduzir_para_portugues(reply)
        history.append({"role": "assistant", "content": reply})
        await message.reply_text(reply) # type:ignore
        await chat_history.add_history(user_id, history)
    except Exception as e:
        print("Erro na resposta de IA: ", e)
        reply = "Desculpe, não estou disponível no momento."
        await message.reply_text(reply) # type:ignore
    finally:
        if sticker: await sticker.delete()

@Client.on_inline_query()  # type:ignore
async def inline_query_handler(client: Client, query: InlineQuery):
    user_data = await users.get_or_add_user(query.from_user.id, query.from_user.first_name)
    query_text = query.query.strip()
    
    if user_data and user_data.get("waiting_for_input"):
        user_data["waiting_for_input"] = False
        await users.update_user(query.from_user.id, user_data)
    else:
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="Aguardando sua entrada",
                    input_message_content=InputTextMessageContent(message_text="Aguardando sua próxima mensagem para responder.")
                )
            ],
            cache_time=0
        )
        user_data["waiting_for_input"] = True
        await users.update_user(query.from_user.id, user_data)
        return

    if not query_text:
        return

    # Processar a query_text para obter a resposta (usando a lógica existente do ai_res)
    response = await get_ai_response([{"role": "user", "content": query_text}])
    response = await traduzir_para_portugues(response)

    # Criar um resultado de consulta inline
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Resposta da IA",
            input_message_content=InputTextMessageContent(message_text=response),
            description="Clique para enviar a resposta da IA"
        )
    ]

    # Responder à consulta inline
    await query.answer(results)
