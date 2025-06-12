import os import asyncio import threading from telethon import TelegramClient, events import telebot from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID")) API_HASH = os.getenv("API_HASH") SESSION = os.getenv("SESSION") INFORCER_BOT = os.getenv("INFORCER_BOT") BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN) client = TelegramClient(SESSION, API_ID, API_HASH)

query_dict = {}

loop = asyncio.new_event_loop() asyncio.set_event_loop(loop)

async def start_telethon(): await client.start() print("Telethon started") await client.run_until_disconnected()

def telethon_thread(): loop.run_until_complete(start_telethon())

@bot.message_handler(commands=['nome']) def handle_nome(message): nome = ' '.join(message.text.split()[1:]) chat_id = message.chat.id if not nome: bot.send_message(chat_id, 'isim gir') return

bot.send_message(chat_id, f"'{nome}' bekle kanks sorgulaniuor")
query_dict[chat_id] = nome

asyncio.run_coroutine_threadsafe(send_query(nome), loop)

async def send_query(nome): await client.send_message(INFORCER_BOT, f"/nome {nome}")

@client.on(events.NewMessage(from_users=INFORCER_BOT)) async def handler(event): if not query_dict: return chat_id, nome = next(iter(query_dict.items())) if event.message.document: file_path = await event.message.download_media() with open(file_path, 'rb') as f: bot.send_document(chat_id, f) del query_dict[chat_id]

if name == "main": threading.Thread(target=telethon_thread, daemon=True).start() bot.infinity_polling()

