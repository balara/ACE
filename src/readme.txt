Run ngnx
run gunicorn  gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app
