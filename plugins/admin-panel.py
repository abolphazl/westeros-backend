from pyrogram import Client, filters
from . import env


# update database
@Client.on_message(filters.command("replace") & filters.private & filters.reply & filters.user(env.admins))
async def updater(client, message):

	database = message.reply_to_message
	user_id = message.from_user.id

	post = await message.reply_text("Please wait...")
	
	try:
		await client.send_document(user_id, env.db_path, caption="last backup")
	except:
		pass

	await client.download_media(database, file_name = env.db_path)

	await post.delete()
	await message.reply_text("done.")




@Client.on_message(filters.command("backup") & filters.private & filters.user(env.admins))
async def backup(client, message):
	try:
		post = await message.reply_text("uploading...")
		await client.send_document(message.from_user.id, env.db_path)
		await post.delete()
	except:
		await post.delete()
		await message.reply_text("database not found!")




# @Client.on_message(filters.command("append") & filters.private & filters.reply & filters.user(env.admins))
# async def appender(client, message):

# 	database = message.reply_to_message
# 	user_id = message.from_user.id

# 	post = await message.reply_text("Please wait...")
	
# 	try:
# 		await client.send_document(user_id, env.db_path, caption="last backup")
# 	except:
# 		pass

# 	await client.download_media(database, file_name = env.container_path)

# 	docs = TinyDB(env.db_path).table("anime_docs")
# 	container = TinyDB(env.container_path)

# 	for item in container.all():
# 		docs.insert({
# 			"anime_id": item["anime_id"],
# 			"mid": item["mid"],
# 			"number": item["number"],
# 			"quality": item["quality"],
# 			"hardsub": item["hardsub"],
# 			"origin": item["origin"]
# 		})

# 	try:
# 		os.remove(env.container_path)
# 		await post.delete()
# 	except:
# 		pass

# 	await message.reply_text("appended")