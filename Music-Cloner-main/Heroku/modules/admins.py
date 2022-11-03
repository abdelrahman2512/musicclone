from asyncio import QueueEmpty

from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

from pyrogram import Client, filters
from pyrogram.types import Message

from Heroku.config import que
from Heroku.core.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from Heroku.calls import calls
from Heroku.setup.filters import command, other_filters
from Heroku.setup.decorators import sudo_users_only
from Heroku.calls.queues import clear, get, is_empty, put, task_done


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


@Client.on_message(command(["pause", "اسكت"]) & other_filters)
async def pause(app: Client, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            "• مفيش حاجه شغاله اصلا."
        )
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text(
            "• مفيش حاجه شغاله اصلا.."
        )
    await music_off(chat_id)
    await calls.pytgcalls.pause_stream(chat_id)
    await message.reply_text(
        f"• تم ايقاف الموسيقى مؤقتا \n بواسطة : {checking}"
    )


@Client.on_message(command(["resume", "استئناف", "كمل"]) & other_filters)
async def resume(app: Client, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(
            "❌ __**لا أعتقد أنه تم إيقاف شيء ما مؤقتًا في الدردشة الصوتية**__"
        )
    elif await is_music_playing(chat_id):
        return await message.reply_text(
            "❌ __**لا أعتقد أنه تم إيقاف شيء ما مؤقتًا في الدردشة الصوتية**__"
        )
    else:
        await music_on(chat_id)
        await calls.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            f"• تم استئناف التشغيل \n بواسطة : {checking}"
        )


@Client.on_message(command(["end", "ايقاف"]) & other_filters)
async def stop(app: Client, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await calls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text(
            f"• تم ايقاف التشغيل \n بواسطة : {checking}"
        )
    else:
        return await message.reply_text(
            "❌ __**لا أعتقد إذا كان هناك شيء ما يتم تشغيله في الدردشة الصوتية**__"
        )


@Client.on_message(command(["skip", "تخطي"]) & other_filters)
async def skip(app: Client, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    checking = message.from_user.mention
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
        await message.reply_text("❌ __**مفيش حاجه شغاله اصلا**__")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text(
                "❌ __**لا مزيد من الموسيقى في قائمة الانتظار**__\n\n**»** `جاري ترك الدردشة الصوتية...`"
            )
            await calls.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await calls.pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        get(chat_id)["file"],
                    ),
                ),
            )
            await message.reply_text(
                f"• تم التخطي \n بواسطة : {checking}"
            )


@Client.on_message(filters.command(["cleandb"]))
async def stop_cmd(app: Client, message):
    if message.sender_chat:
        return await message.reply_text(
            "🔴 __أنت **مشرف مجهول**!__\n│\n╰ عد إلى حساب المستخدم من حقوق المسؤول."
        )
    permission = "can_delete_messages"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    chat_id = message.chat.id
    checking = message.from_user.mention
    try:
        clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)
    try:
        await calls.pytgcalls.leave_group_call(chat_id)
    except:
        pass
    await message.reply_text(
        f"✅ __قوائم الانتظار المحذوفة بتنسيق **{message.chat.title}**__\n│\n╰ تم تنظيف قاعدة البيانات بواسطة {checking}"
    )
