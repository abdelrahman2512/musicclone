from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from Heroku.config import BOT_NAME, OWNER_USERNAME, UPDATE, SUPPORT, BOT_USERNAME

IMG = ["https://telegra.ph/file/9cbae99908382932e51f0.png", "https://telegra.ph/file/9870433b0c155ecf2ad07.png", "https://telegra.ph/file/c6efbd77d1d931c45d0c2.jpg", "https://telegra.ph/file/f9d97a7cde8b79f4ab0a3.png"]
HELP_TEXT = """
مرحبا ! [{}](tg://user?id={})
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
✘ أنا بوت تشغيل موسيقي في المكالمه الصوتيه ولدي الكثير من الميزات التي تعجبك
‣ أستطيع تشغيل ( الصوت + الفيديو )
‣ لدي تقريبًا جميع الميزات التي تحتاجها في بوت الموسيقى
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
✘ انقر فوق زر المساعدة لمزيد من المعلومات.
"""


@Client.on_callback_query(filters.regex("home"))
async def home(_, query: CallbackQuery):
    await query.edit_message_text(f"{HELP_TEXT}".format(query.message.chat.first_name, query.message.chat.id),
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                    "➕ اضفني الى مجموعتك", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],
                [
                    InlineKeyboardButton(
                        "𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀", url=f"https://t.me/JAVA_telthon"),
                    InlineKeyboardButton(
                    "المساعدة", callback_data="others") 
                ]
           ]
        ),
    )






@Client.on_callback_query(filters.regex("others"))
async def others(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""مرحبا [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

انقر فوق الأزرار الواردة أدناه لمعرفة المزيد عني :""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀", url=f"https://t.me/JAVA_telthon"),
                    InlineKeyboardButton(
                        "𝐒𝐀𝐋𝐀𝐇 𝐇𝐄𝐌𝐃𝐀𝐍", url=f"https://t.me/Salah_officiall")
                ],
                [
                    InlineKeyboardButton(
                        "اوامر التشغيل 🖇", callback_data="credit"),
                ],
                [
                    InlineKeyboardButton(
                    "الدليل الأساسي ⁉️", callback_data="cbhowtouse") 
                ],
                [       
                    InlineKeyboardButton(
                        "السورس", callback_data="repoinfo")
                ],
                [
                    InlineKeyboardButton("⬅️ رجــوع", callback_data="home")
                ]
           ]
        ),
    )


@Client.on_callback_query(filters.regex("credit"))
async def credit(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**🤖 أوامر البوت العادية :-

» /play او تشغيل و (اسم الاغنيه)  - لتشغيل الموسيقي
» /skip - تخطي الأغنية
» /end - ايقاف تشغيل الموسيقى
» /pause - أوقف التشغيل مؤقتًا
» /resume - استئناف التشغيل
» /mute - كتم المساعد 
» /search - (إسم الأغنية)



⚙ بعض الأوامر الإضافية :-

» /examine - لاختبار حالة تشغيل البوت
» /start - بدأ البوت
» /id - لجلب ايديك
» /repo - لجلب كود مصدر السورس
» /rmd - حذف كل التنزيلات
» /clean - نظف ملفات التخزين
» /gcast - بث رسالتك**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅️ رجــوع", callback_data="others")
                ],
            ]
        ),
    )

@Client.on_callback_query(filters.regex("cls"))
async def reinfo(_, query: CallbackQuery):
    try:
        await query.message.delete()
        await query.message.reply_to_message.delete()
    except Exception:
        pass

@Client.on_callback_query(filters.regex("cbhowtouse"))
async def repoinfo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **الدليل الأساسي لاستخدام هذا الروبوت:**
\n\n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════• \n\n
1.) **أولا ، أضفني إلى مجموعتك.**
2.) **بعد ذلك ، قم بترقيتي كمسؤول ومنح جميع الأذونات باستثناء المسؤول المجهول.**
3.) **بعد ترقيتي ، اكتب /reload في مجموعة لتحديث بيانات المسؤولين.**
3.) **اضف @{ASSISTANT_NAME} إلى مجموعتك أو اكتب / userbotjoin لدعوته.**
4.) **قم بتشغيل مكالمة صوتيه أولاً قبل البدء في تشغيل الفيديو / الموسيقى.**
5.) **في بعض الأحيان ، يمكن أن تساعدك إعادة تحميل الروبوت باستخدام الأمر / reload في إصلاح بعض المشكلات.**
\n\n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════• \n\n
📌 **إذا لم ينضم المساعد إلى الدردشة المرئية ، فتأكد من تشغيل دردشة الفيديو بالفعل ، أو اكتب / userbotleave ثم اكتب / userbotjoin مرة أخرى.\n\n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════• \n\n**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅️ رجــوع", callback_data="others")
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex("repoinfo"))
async def repoinfo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""سورس جافا ميوزك \n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════• \n• مبرمج السورس : [ 𝐒𝐀𝐋𝐀𝐇 𝐇𝐄𝐌𝐃𝐀𝐍 ](https://t.me/Salah_officiall) \n• قناة السورس : [ 𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀 ](https://t.me/JAVA_tlethon) \n• جروب الدعم : [ 𝐉𝐀𝐕𝐀 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 ](https://t.me/JAVA_tlethon) \n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════•""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⬅️ رجــوع", callback_data="others")
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
