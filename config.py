import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OAUTH_PROVIDERS = [
    {'name': 'Google', 'url': 'login/google'},
    {'name': 'Facebook', 'url': 'login/facebook'}
    ]

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '236507713421072',
        'secret': '75cb7fb97ea05ea1f27f14e0fd5605df'
    }}

SQLALCHEMY_DATABASE_URI = 'mysql://manuelgm:mko0nji9@manuelgm.mysql.pythonanywhere-services.com/manuelgm$default'
SQLALCHEMY_MIGRATE_REPO = os.path.join('/home/manuelgm/mysite/db_repository')

# pagination
POSTS_PER_PAGE = 10

