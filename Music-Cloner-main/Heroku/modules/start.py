import asyncio

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, UserNotParticipant
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

from time import time
from datetime import datetime

from Heroku.setup.filters import command
from Heroku.config import BOT_NAME, OWNER_USERNAME, UPDATE, SUPPORT, BOT_USERNAME

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)

IMG = ["https://telegra.ph/file/9cbae99908382932e51f0.png", "https://telegra.ph/file/9870433b0c155ecf2ad07.png", "https://telegra.ph/file/c6efbd77d1d931c45d0c2.jpg", "https://telegra.ph/file/f9d97a7cde8b79f4ab0a3.png"]
HELP_TEXT = """
مرحبا ! {}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
✘ أنا بوت تشغيل موسيقي في المكالمه الصوتيه ولدي الكثير من الميزات التي تعجبك
‣ أستطيع تشغيل ( الصوت + الفيديو )
‣ لدي تقريبًا جميع الميزات التي تحتاجها في بوت الموسيقى
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
✘ انقر فوق زر المساعدة لمزيد من المعلومات ℹ️.
"""


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(f"{HELP_TEXT}".format(message.from_user.mention()),
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ اضفني الى مجموعتك", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    InlineKeyboardButton(
                        "𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀", url=f"https://t.me/{UPDATE}"),
                    InlineKeyboardButton(
                        "المساعدة ⁉️", callback_data="others")
                ]
           ]
        ),
    )



@Client.on_message(command(["ping","البينج"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("✧ جاري حساب سرعة البوت...")
    delta_ping = time() - start
    await m_reply.edit_text("✧ سرعة البوت : \n✧ " f"`{delta_ping * 1000:.3f} MS`")
