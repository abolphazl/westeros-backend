# Westeros Telegram Bot
username = @westeros_robot

### Setup
```bash
# generate vertual env
$ python3 -m venv .venv
$ source .venv/bin/activate

# install requirements
$ pip install -r requirements.txt

# create .env file and put your API_ID, API_HASH and BOT_TOKEN in .env

# generate main session
$ python session-gen.py main

# run wsgi.py & bot.py using tmux or screen or etc...
$ sudo python wsgi.py # run as sudo!
$ python bot.py
```

### Todo List
- [ ] Admin panel
- [ ] Auto setup
- [ ] Lite version
- [ ] Multiple language
- [ ] Subtitle support
