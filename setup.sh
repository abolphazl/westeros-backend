
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

if [ ! -d "./data" ]; then
  mkdir data
fi

source .venv/bin/activate

pip install -r requirements.txt

if [ ! -f "./data/main.session" ]; then
  python session-gen.py main
fi

if [ ! -f "./data/helper.session" ]; then
  python session-gen.py helper
fi


python wsgi.py &
echo $! > pid.txt

python bot.py &
echo $! >> pid.txt