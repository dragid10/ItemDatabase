# Getting started

1. Install dependenciesd
   
```shell
pip install -r deps/requirements.dev
pip-sync requirements*
```

2. Have a sqlite database?

```shell
sqlite3  database.db < create_tables.sql
```

3. Run the GUI and API seperately?

```shell
# Run API server
fastapi dev main.py

# Run GUI
python3 -m gui.main
```
