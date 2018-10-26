uwsgi --plugin python3 --socket 127.0.0.1:3031 --wsgi-file manage.py --callable app --processes 4 --threads 4 --stats 0.0.0.0:9191 --py-autoreload=1
