import os
import json
from utilities.key_grabber import get_secret

PLATOFORMS_TOKEN = json.loads(get_secret(os.environ.get('PLATO_FORMS_TOKEN_RESOURCE')).get('SecretString')).get('platoToken')
ATHENA_TOKEN = json.loads(get_secret(os.environ.get('ATHENA_PROXY_TOKEN_RESOURCE')).get('SecretString')).get('token')
AURORA_REPO_CREDS = json.loads(get_secret(os.environ.get('AURORA_RESOURCE'))

AURORA_USER = AURORA_REPO_CREDS['username']
AURORA_PASSWORD = AURORA_REPO_CREDS['password']
AURORA_HOST = AURORA_REPO_CREDS['host']
AURORA_DATABASE = 'dna_athena'

AURORA_REPO_URI = f'postgresql://{AURORA_USER}:{AURORA_PASSWORD}@{AURORA_HOST}:5432/{AURORA_DATABASE}'