find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
echo "The database has been reset. Please remember to create a new superuser by typing in the command: \"python manage.py createsuperuser\" before running the server."
python manage.py createsuperuser