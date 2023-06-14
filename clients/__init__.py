import os
from .athena import AthenaProxyClient, AthenaClient
from .platoform import PlatoFormsClient
from settings import ATHENA_TOKEN, PLATOFORMS_TOKEN, PROD

if PROD:
    ATHENA_URL = os.environ.get('ATHENA_BASE_URL')
else:
    ATHENA_URL = os.environ.get('ATHENA_PREVIEW_BASE_URL')
   
ATHENA_PROXY_URL = os.environ.get('ATHENA_PROXY_BASE_URL')

athena_proxy_client = AthenaProxyClient(ATHENA_PROXY_URL, ATHENA_TOKEN)
athena_token = athena_proxy_client.get_token()
athena_client = AthenaClient(ATHENA_URL, athena_token)
platoform_client = PlatoFormsClient(PLATOFORMS_TOKEN)
