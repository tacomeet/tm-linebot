import os


def get_db_uri():
    uri = os.environ.get('DATABASE_URL')
    if uri is None:
        db_user = os.environ['DB_USER']
        db_password = os.environ['DB_PASSWORD']
        db_host = os.environ['DB_HOST']
        db_port = os.environ['DB_PORT']
        db_name = os.environ['DB_NAME']
        uri = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=disable'
    return uri
