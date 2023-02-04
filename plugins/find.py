from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from tinydb import TinyDB, Query, where
from pyrogram import Client, filters
from uuid import uuid4
from . import env
import subprocess
import jellyfish
import re, os




def searcher_helper(title, text):
	text  = re.sub("[^ A-Za-z1-9]", "", text)
	title = re.sub("[^ A-Za-z1-9]", "", title)

	lim = jellyfish.jaro_distance(text.lower(), title.lower())

	if lim >= 0.70:
		return True


async def searcher(message, text):

	movies = TinyDB(env.db_path).table("movies")
	user_id = message.from_user.id

	try:
		search_result = movies.search((Query().title.test(searcher_helper, text)))
		if len(search_result) == 0: raise "Not Found!"
	except Exception as e:
		await message.reply_text(env.not_found)
		return False

	
	keyboards = []
	for item in search_result:
		keyboards.append(
            [
                KeyboardButton(item['title'], web_app = WebAppInfo(url = env.url.format(imdb_id=item["imdb_id"], user_id=message.from_user.id)))
            ]
        )
		
	reply_markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
	return reply_markup
	


@Client.on_message(filters.text & filters.private & ~filters.command(env.commands))
async def find_by_text(_, message):
	text = message.text
	search_result = await searcher(message, text)
	if search_result == False: return
	await message.reply_text(env.results, reply_markup = search_result)

	
@Client.on_message(filters.photo & filters.private)
async def find_anime_by_photo(_, message):
	post = await message.reply_text(env.downloading)
	file_name = str(uuid4())
	await message.download(env.data_path + f"/{file_name}.jpg")
	args = ["./plugins/what-anime-cli", "file", env.data_path + f"/{file_name}.jpg"]
	
	try:
		await post.edit(env.photo_process)
		command = str(subprocess.run(args, capture_output=True, text=True).stdout)
		os.remove(env.data_path + f"/{file_name}.jpg")
		data = re.match(".*English: ([\w\d\s]*) .*", command.replace("\n", " "))
		title = data.group(1)
	except Exception as e:
		await post.edit(env.photo_err)
		return

	await post.delete()
	search_result = await searcher(message, title)
	if search_result == False: return
	await message.reply_text(env.photo_results.format(title=title), reply_markup = search_result)

