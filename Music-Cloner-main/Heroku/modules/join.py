import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait

from Heroku import ASSUSERNAME
from Heroku.setup.decorators import sudo_users_only, errors
from Heroku.setup.administrator import adminsOnly
from Heroku.setup.filters import command
from Heroku.calls import client as USER


@Client.on_message(
    command(["userbotjoin", f"ادخل"]) & ~filters.private & ~filters.bot
)
@errors
async def addchannel(client, message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chid = message.chat.id
    try:
        invite_link = await message.chat.export_invite_link()
        if "+" in invite_link:
            kontol = (invite_link.replace("+", "")).split("t.me/")[1]
            link_bokep = f"https://t.me/joinchat/{kontol}"
    except:
        await message.reply_text(
            "**ارفعني مشرف الاول يا اعمى القلب والنظر**",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = f"{ASSUSERNAME}"

    try:
        await USER.join_chat(link_bokep)
    except UserAlreadyParticipant:
        await message.reply_text(
            f"🔴 **{user.first_name} انضم بالفعل إلى هذه المجموعة !!**",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"❌ **مساعد ({user.first_name}) لا يمكن الانضمام إلى مجموعتك بسبب العديد من طلبات الانضمام للمساعد !**\n‼️ تأكد من عدم حظر حساب المساعد في المجموعة."
            f"\n\n» `قم يدويًا بإضافة {user.first_name} إلى مجموعتك`",
        )
        return


@USER.on_message(filters.group & command(["userbotleave", "غادر", "odaleft"]))
async def rem(USER, message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    try:
        await USER.send_message(
            message.chat.id,
            "✅ غادر المساعد المجموعه بنجاح....",
        )
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "❌ **لا يمكن للمساعد مغادرة مجموعتك!**\n\n» ازلني يدويًا من مجموعتك</b>"
        )

        return


@Client.on_message(command(["غادر الكل", "leaveall"]))
@sudo_users_only
async def bye(client, message):
    left = 0
    sleep_time = 0.1
    lol = await message.reply("**يغادر المساعد جميع الجروبات**\n\n`انتظر قليلا...`")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            await asyncio.sleep(sleep_time)
            left += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await lol.edit(f"🏃‍♂️ `غادر المساعد بنجاح...`\n\n» **غادر:** {left} مجموعه.")
