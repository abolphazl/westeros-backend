from dotenv import load_dotenv
from pyrogram import Client
from plugins import env
import sys, os

# check point
if not os.path.exists(env.data_path):
    os.makedirs(env.data_path)

if len(sys.argv) != 2:
    print("ERROR: argument count is incorrect!")
    quit()


# generate session
load_dotenv()
session = Client(
    env.data_path + '/' + sys.argv[1],
    api_id    = os.getenv("API_ID"),
    api_hash  = os.getenv("API_HASH"),
    bot_token = os.getenv("BOT_TOKEN"),
)

with session:
    print(f"@{session.get_me().username} session generated! ({sys.argv[1]})")