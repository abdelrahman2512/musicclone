import aiofiles
import ffmpeg
import asyncio
import os
import shutil
import psutil
import subprocess
import requests
import aiohttp
import yt_dlp
import aiohttp
import random

from os import path
from typing import Union
from asyncio import QueueEmpty
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from typing import Callable

from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

from youtube_search import YoutubeSearch

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    Voice,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


from Heroku import BOT_NAME, BOT_USERNAME
from Heroku.calls import calls, queues
from Heroku.calls.youtube import download
from Heroku.calls import convert as cconvert
from Heroku.calls.calls import client as ASS_ACC
from Heroku.core.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
import Heroku.calls
from Heroku.calls import youtube
from Heroku.config import (
    DURATION_LIMIT,
    que,
    SUDO_USERS,
    BOT_ID,
    ASSNAME,
    ASSUSERNAME,
    ASSID,
    SUPPORT,
    UPDATE,
    BOT_NAME,
    START_PIC,
    BOT_USERNAME,
)
from Heroku.setup.filters import command
from Heroku.setup.decorators import errors, sudo_users_only
from Heroku.setup.administrator import adminsOnly
from Heroku.setup.errors import DurationLimitError
from Heroku.setup.gets import get_url, get_file_name
from Heroku.modules.admins import member_permissions


# plus
chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
flex = {}


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 27:        
            text1 += " " + i
        elif len(text2) + len(i) < 25:        
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]

# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image = Image.open(f"./background.png")
    black = Image.open("etc/black.jpg")
    img = Image.open("etc/robot.png")
    image5 = changeImageSize(1280, 720, img)
    image1 = changeImageSize(1280, 720, image)
    image1 = image1.filter(ImageFilter.BoxBlur(10))
    image11 = changeImageSize(1280, 720, image)
    image1 = image11.filter(ImageFilter.BoxBlur(10))
    image2 = Image.blend(image1,black,0.6)

    # Cropping circle from thubnail
    image3 = image11.crop((280,0,1000,720))
    #lum_img = Image.new('L', [720,720] , 0)
   # draw = ImageDraw.Draw(lum_img)
   # draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
   # img_arr =np.array(image3)
    #lum_img_arr =np.array(lum_img)
    #final_img_arr = np.dstack((img_arr,lum_img_arr))
    #image3 = Image.fromarray(final_img_arr)
    image3 = image3.resize((500,500))
    

    image2.paste(image3, (100,115))
    image2.paste(image5, mask = image5)

    # fonts
    font1 = ImageFont.truetype(r'etc/robot.otf', 30)
    font2 = ImageFont.truetype(r'etc/robot.otf', 60)
    font3 = ImageFont.truetype(r'etc/robot.otf', 49)
    font4 = ImageFont.truetype(r'etc/Mukta-ExtraBold.ttf', 35)

    image4 = ImageDraw.Draw(image2)

    # title
    title1 = truncate(title)
    image4.text((670, 280), text=title1[0], fill="white", font = font3, align ="left") 
    image4.text((670, 332), text=title1[1], fill="white", font = font3, align ="left") 

    # description
    views = f"Views : {views}"
    duration = f"Duration : {duration} minutes"
    channel = f"Request : {BOT_NAME} Bot"

    image4.text((670, 410), text=views, fill="white", font = font4, align ="left") 
    image4.text((670, 460), text=duration, fill="white", font = font4, align ="left") 
    image4.text((670, 510), text=channel, fill="white", font = font4, align ="left")

    
    image2.save(f"final.png")
    os.remove(f"background.png")
    final = f"temp.png"
    return final
     



# play
@Client.on_message(
    command(["play", f"تشغيل"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(app: Client, message: Message):
    global que
    global useer
    user_id = message.from_user.id
    if message.sender_chat:
        return await message.reply_text(
            " __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المشرف"
        )

    if message.chat.id in DISABLED_GROUPS:
        await message.reply(
            " __**تم إيقاف تشغيل مشغل الموسيقى ، اطلب من المشرف تشغيله!**__"
        )
      

        return
    lel = await message.reply("🔄 جاري تنفيذ طلبك ... الرجاء الانتظار!")

    chid = message.chat.id
    aing = await app.get_me()
    c = await app.get_chat_member(message.chat.id, aing.id)
    if c.status != "administrator":
        await lel.edit(
            f"**انت متأكد انك رافعني مشرف  ؟!!**"
        )
        return
    if not c.can_manage_voice_chats:
        await lel.edit(
            "**ليس لدي صلاحية : إدارة الدردشة الصوتية**"
        )
        return
    if not c.can_delete_messages:
        await lel.edit(
            "**ليس لدي صلاحية : حذف الرسائل**"
        )
        return
    if not c.can_invite_users:
        await lel.edit(
            "**ليس لدي صلاحية : اضافة مستخدمين**"
        )
        return

    try:
        b = await app.get_chat_member(message.chat.id, ASSID)
        if b.status == "kicked":
            await message.reply_text(
                f"🔴 {ASSNAME} (@{ASSUSERNAME}) تم حظره في الدردشة الخاصة بك **{message.chat.title}**\n\nقم بإلغاء الحظر أولاً لاستخدامي"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(f"{message.chat.username}")
                await message.reply(
                    f"**@{ASSUSERNAME} انضم بنجاح !**",
                )
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(
                    f"**@{ASSUSERNAME} فشل في الانضمام** اضف @{ASSUSERNAME} يدويا في مجموعتك.\n\n**سبب فشل انضمام المساعد **: {e}"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    kontol = (invite_link.replace("+", "")).split("t.me/")[1]
                    link_bokep = f"https://t.me/joinchat/{kontol}"
                await ASS_ACC.join_chat(link_bokep)
                await message.reply(
                    f"**@{ASSUSERNAME} هنا بالفعل عزيزي**",
                )
                await remove_active_chat(message.chat.id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"**@{ASSUSERNAME} فشل في الانضمام** اضف @{ASSUSERNAME} يدويا في مجموعتك.\n\n**سبب فشل انضمام المساعد **: {e}"
                )

    await message.delete()
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"✧ مقطع الفيديو أطول من {DURATION_LIMIT} الدقائق غير مسموح بها!"
            )

        file_name = get_file_name(audio)
        url = f"https://t.me/{UPDATE}"
        title = audio.title
        thumb_name = "https://telegra.ph/file/a7adee6cf365d74734c5d.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("⚙️ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url=f"t.me/{SUPPORT}"),
            InlineKeyboardButton("🖇 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url=f"t.me/{UPDATE}"),
        ],[
            InlineKeyboardButton("🎥 𝗪𝗮𝘁𝗰𝗵 𝗼𝗻 𝗬𝗼𝘂𝗧𝘂𝗯𝗲", url=f"{url}"),
        ],[
            InlineKeyboardButton("❌️ 𝗖𝗹𝗼𝘀𝗲", callback_data="cls"),
        ],
        
    ]
)

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await cconvert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
    [
        
       [
            InlineKeyboardButton("⚙️ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url=f"t.me/{SUPPORT}"),
            InlineKeyboardButton("🖇 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url=f"t.me/{UPDATE}"),
        ],[
            InlineKeyboardButton("🎥 𝗪𝗮𝘁𝗰𝗵 𝗼𝗻 𝗬𝗼𝘂𝗧𝘂𝗯𝗲", url=f"{url}"),
        ],[
            InlineKeyboardButton("❌️ 𝗖𝗹𝗼𝘀𝗲", callback_data="cls"),
        ],
        
    ]
)

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/a7adee6cf365d74734c5d.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="YouTube 🎬", url=f"{url}")]]
            )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"✧ مقطع الفيديو أطول من {DURATION_LIMIT} الدقائق غير مسموح بها!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                        print(
                            f"✧ [{url_suffix}] تم التنزيل {percentage}\n✧ بسرعة {speed} | و : {eta} ثانيه"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                        print(
                            f"✧ [{url_suffix}] تم التنزيل {percentage} بسرعة {speed} | و : {eta} ثانيه"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                        print(
                            f"✧ [{url_suffix}] تم التنزيل {percentage} بسرعة {speed} | و : {eta} ثانيه"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"**جارى التحميل :** {title[:50]}.....\n\n✧ **الاسم :** {size}\n✧ **الوقت :** {taken} sec\n\n✧ **تحويل الملف : **[__FFmpeg processing__]"
                )
                print(f"✧ [{url_suffix}] تم تنزيله في: {taken} ثانيه")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert(x)
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**اكتب **: /play [اسم الموسيقى أو رابط يوتيوب أو الرد على الصوت]"
            )
        await lel.edit("**🔄 جاري تنفيذ امرك ... الرجاء الانتظار!**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**جاري استدعاء المساعد للمكالمة الصوتيه**")
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "✧ **لم يتم العثور على الاغنية**\n\nاكتب الاسم بشكل صحيح."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
    [
       [
            InlineKeyboardButton("📂 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url=f"t.me/{SUPPORT}"),
            InlineKeyboardButton("✨ 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url=f"t.me/{UPDATE}"),
        ],[
            InlineKeyboardButton("🎥 𝗪𝗮𝘁𝗰𝗵 𝗼𝗻 𝗬𝗼𝘂𝗧𝘂𝗯𝗲", url=f"{url}"),
        ],[
            InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="cls"),
        ],
        
    ]
)

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"✧ مقطع الفيديو أطول من {DURATION_LIMIT} الدقائق غير مسموح بها!"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            lel.edit(
                                f"جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                    except Exception as e:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                        print(
                            f"✧ [{url_suffix}] تم التنزيل {percentage}\n✧ بسرعة {speed} \n✧ الثواني : {eta} ثانيه"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                        print(
                            f"✧ [{url_suffix}] تم التنزيل {percentage}\n✧ بسرعة {speed} \n✧ الثواني : {eta} ثانيه"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            lel.edit(
                                f"**جارى التحميل {title[:50]}\n\n✧ **حجم الملف :** {size}\n✧ **تقدم :** {percentage}\n✧ **السرعة :** {speed}\n✧ **الثواني :** {eta} ثانيه"
                            )
                        print(
                            f"✧ [{url_suffix}] تم التنزيل {percentage}\n✧ بسرعة : {speed} \n✧ الثواني: {eta} ثانيه"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception as e:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                lel.edit(
                    f"**انتهى التنزيل !!**\n\n✧ **{title[:50]}...\n\n✧** حجم الصوت : {size}**\n\n✧ **الوقت المستغرق : {taken} ثانيه"
                )
                print(f"✧ [{url_suffix}] تم التنزيل في : {taken} ثانيه")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, url, my_hook)
        file_path = await cconvert(x)

    if await is_active_chat(message.chat.id):
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="تم اضافتها لقائمة الانتظار {}\n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════•\n\n**📂 الاسم :**[{}]({})\n\n📈 **حالة التشغيل :** `انتظار`\n📌 **نوع التشغيل :** `موسيقي`\n👥 طلب : {}\n\n•═════•| [ 𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪 ](https://t.me/JAVA_tlethon) |•═════•".format(
                position, title, url, message.from_user.mention()
            ),
        )
    else:
        try:
            await calls.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception:
            return await lel.edit(
                "✧ خطأ في الانضمام إلى الدردشة الصوتية. تأكد من تمكين الدردشة الصوتية.\n\n✧ إذا كانت الإجابة بنعم ، فتأكد من أن حساب المساعد ليس محظورًا في مجموعتك أو متاحًا في مجموعتك!"
            )


        await music_on(message.chat.id)
        await add_active_chat(message.chat.id)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**تم التشغيل بنجاح \n•═════•| [𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪](https://t.me/JAVA_tlethon) |•═════•\n\n📁 **الاسم :** [{}]({})\n🖇 **الوقت :** `{duration}`\n📈 **حالة التشغيل :** `شغال`\n📌 **نوع التشغيل :** `موسيقي`\n👤 **مطلوبه بواسطة :** {}\nللمزيد من المعلومات : [اضغط هنا](https://t.me/JAVA_Supports)\n\n•═════•| [𓆩𝐒𝐎𝐔𝐑𝐂𝐄 𝐉𝐀𝐕𝐀𓆪](https://t.me/JAVA_tlethon) |•═════•".format(
                title, url, message.from_user.mention()
            ),
        )
    try:
        os.remove("final.png")
    except Exception:
        pass
    return await lel.delete()
