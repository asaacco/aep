# modules/auth/google_oauth.py
import os
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'default-client-id')

def verify_google_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID)
        return {
            'email': id_info['email'],
            'name': id_info.get('name', ''),
            'picture': id_info.get('picture', '')
        }
    except ValueError:
        return None