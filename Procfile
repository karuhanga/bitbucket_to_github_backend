release: python manage.py migrate
worker: celery -A bitbucket_github worker -l error --without-gossip --without-mingle --without-heartbeat
web: gunicorn project.wsgi --log-file -
heroku ps:scale worker=1
