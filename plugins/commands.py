from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove
from pyrogram import Client, filters
from tinydb import TinyDB, where
from . import env



async def user_check(message):
	members = TinyDB(env.db_path).table("members")
	if members.contains(where("user_id") == message.from_user.id):
		return
	
	members.insert({
		"user_id": message.from_user.id,
		"status": None,
		"mem": None,
	})

	await message.reply_text(env.new_user.format(fname=message.from_user.first_name))


async def subcommand_send_file(client, message, mid):
	await client.copy_message(message.from_user.id, env.docs_channel, mid, caption="")


async def subcommand_process(client, message):
	sub = message.command[1]
	try:
		cake = sub.split("-")
		work_type = cake[0]
		work_id = int(cake[1])
		if work_type not in ["file", "movie"]: return False
	except Exception as e:
		print(e)
		return False
	
	if work_type == "file": await subcommand_send_file(client, message, work_id)


# Start
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
	await user_check(message)
	
	# sub commands
	if len(message.command) == 2:
		if await subcommand_process(client, message) == False:
			await message.reply_text(env.start, reply_markup=ReplyKeyboardRemove(True))
	else:
		await message.reply_text(env.start, reply_markup=ReplyKeyboardRemove(True))


# List
@Client.on_message(filters.command("list") & filters.private)
async def show_anime_list(_, message):
	movies = TinyDB(env.db_path).table("movies")
	bookmarks = TinyDB(env.db_path).table("bookmarks")

	user_id = message.from_user.id
	user_bookmarks = bookmarks.search(where("user_id") == user_id)

	keyboards = []
	for item in user_bookmarks:
		movie = movies.get(where("imdb_id") == item['imdb_id'])
		keyboards.append(
			[
				KeyboardButton(movie['title'], web_app = WebAppInfo(url = env.url.format(imdb_id=movie['imdb_id'], user_id=message.from_user.id)))
			]
		)

	if len(keyboards) == 0:
		await message.reply_text(env.bookmarks_is_empty)
		return

	reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
	await message.reply_text(env.your_fav, reply_markup = reply_markup)


@Client.on_message(filters.command("help") & filters.private)
async def help(_, message):
	await message.reply_text(env.help_message)


