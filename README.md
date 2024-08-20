# Getting started

This project uses python 3.12 and is still very much a WIP

1. Install dependenciesd
   
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r deps/dev-requirements.in
pip-sync --python-executable .venv/bin/python requirements*
```

2. Have a sqlite database?

```shell
touch database.db
```

3. Run the GUI and API seperately?

```shell
# Run API server
fastapi dev main.py

# Run GUI
python3 -m gui.main
```
