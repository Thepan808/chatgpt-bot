# ©️biisal jai shree krishna 😎
from pyrogram.client import Client
from pyrogram.handlers import InlineQueryHandler
from info import *

class Bot(Client):
    def __init__(self):
        super().__init__( # type:ignore
            name="Bisal Gptt",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        self.add_handler(InlineQueryHandler(inline_query_handler))

    async def start(self): # type:ignore
        await super().start()
        me = await self.get_me()
        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")
        await self.send_message(ADMIN, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")

    async def stop(self, *args): # type:ignore
        await super().stop()
        print("Bᴏᴛ Iꜱ Sᴛᴏᴘᴘᴇᴅ....")

Bot().run() # type:ignore
