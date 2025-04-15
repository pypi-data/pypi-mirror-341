from cryptography.fernet import Fernet
import os
import yaml
import zipimport
from dotenv import load_dotenv, find_dotenv


FERNET_KEY: bytes = None

def set_key(key: bytes):
    global FERNET_KEY
    FERNET_KEY = key

def get_key() -> bytes:
    global FERNET_KEY
    if FERNET_KEY is None:
        dotenv_path = find_dotenv(usecwd=True)
        load_dotenv(dotenv_path)
        
        key_from_env = os.environ.get("FERNET_KEY_SECRET")
        
        if not key_from_env:
            try:
                from airflow.models import Variable
                key_from_env = Variable.get("FERNET_KEY_SECRET", default_var=None)
            except Exception as e:
                pass
        
        if key_from_env:
            FERNET_KEY = key_from_env.encode()
        else:
            raise ValueError("Fernet key has not been set")
    return FERNET_KEY

def get_credentials(
    platform: str,
    account_name: str,
) -> None:
    m = zipimport.zipimporter(
        f'{os.path.dirname(__file__)}/r.zip'
    ).load_module('r')

    c = yaml.safe_load(
        Fernet(
            get_key()
            # m.retrieve()['k'] # thay thế key sẵn có
        ).decrypt(
            m.retrieve()['d']
        )
    ).get(
        platform,
        {
            'error': f'The platform {platform} is not available'
        }
    )
    if 'error' in c:
        raise Exception(c)
    
    c = c.get(
        account_name,
        {
            'error': f'The account {account_name} is not available'
        }
    )
    if 'error' in c:
        raise Exception(c)

    return c
