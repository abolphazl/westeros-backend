from pyrogram import Client, filters
from . import env

@Client.on_message(filters.chat(env.desktop) & filters.document)
async def sign_episode(_, message):
    post = await message.copy(env.docs_channel)
    file_name = post.document.file_name
    post_id = post.id
    await message.delete()
    await message.reply_text(f"`{file_name}`\n`{post_id}`")


@Client.on_message(filters.document & filters.private & filters.user(env.admins))
async def store_file(client, message):
    post = await message.copy(env.docs_channel)
    me = await client.get_me()

    url = f"https://t.me/{me.username}?start=file-{post.id}"

    await message.delete()
    await message.reply_text(f"`{url}`")
