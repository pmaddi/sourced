web: gunicorn runp-heroku:app
init: python db_create.py && pybabel compile -d app/translations
upgrade: python db_upgrade.py && pybabel compile -d app/translations
reset: python db_reset.py && pybabel compile -d app/translations