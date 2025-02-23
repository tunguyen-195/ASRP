import telegram
import asyncio

BOT_TOKEN = '7991446285:AAEsV-s1cBPJKbhUO385MKa6YREUVaBfkcY'
bot = telegram.Bot(token=BOT_TOKEN)

async def get_chat_id():
    updates = await bot.get_updates()
    for update in updates:
        print(update.message.chat.id)

if __name__ == "__main__":

    asyncio.run(get_chat_id())