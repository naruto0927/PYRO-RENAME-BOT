
from datetime import datetime
from pytz import timezone
from pyrogram import Client, version
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
import os

class Bot(Client):
    def init(self):
        super().init(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=min(32, os.cpu_count() + 4),
            plugins={"root": "plugins"},
            sleep_threshold=15,
            max_concurrent_transmissions=Config.MAX_CONCURRENT_TRANSMISSIONS,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = datetime.fromisoformat(Config.BOT_UPTIME)     
        if Config.WEB_SUPPORT:
            app = web.AppRunner(web.Application(client_max_size=30000000))
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", 8080).start()
            
        print(f"\033[1;96m @{me.username} Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️\033[0m")
        try: 
            for id in Config.ADMIN:
                await self.send_message(id, f"{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")                              
        except: pass
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                chat = await self.get_chat(Config.LOG_CHANNEL)
                await self.send_message(chat.id, f"__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!\n\n📅 Dᴀᴛᴇ : {date}\n⏰ Tɪᴍᴇ : {time}\n🌐 Tɪᴍᴇᴢᴏɴᴇ : Asia/Kolkata\n\n🉐 Vᴇʀsɪᴏɴ : v{__version__} (Layer {layer})")                                
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")


Bot().run()
