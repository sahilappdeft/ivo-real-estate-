import requests
from django.conf import settings

FASTAPI_BASE_URL = settings.FASTAPI_BASE_URL

def call_auth_microservice(url, data, token=None):
    # Define the base URL of your FastAPI auth-microservice

     # Define the headers with the token
    headers = {'Authorization': f'Bearer {token}'}
    if not token:
        headers = {}

    response = requests.post(f"{FASTAPI_BASE_URL}{url}", json=data, headers=headers)
    return response


def get_user_info(user_id):
    # Define the base URL of your FastAPI auth-microservice
    response = requests.get(f"{FASTAPI_BASE_URL}/user/{user_id}")
    return response.json()