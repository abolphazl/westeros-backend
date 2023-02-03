# active virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies & run webserver
pip install -r requirements.txt
python wsgi.py