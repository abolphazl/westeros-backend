from pyrogram import Client
from plugins import env

bot = Client(env.main_session_path, plugins=dict(root="plugins"))

if __name__ == "__main__":
    with bot:
        print(f"@{bot.get_me().username} started!")
    bot.run()