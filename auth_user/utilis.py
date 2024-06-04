import requests

def call_auth_microservice(url, data, token=None):
    # Define the base URL of your FastAPI auth-microservice
    FASTAPI_BASE_URL = "http://127.0.0.1:5000"

     # Define the headers with the token
    headers = {'Authorization': f'Bearer {token}'}
    if not token:
        headers = {}

    response = requests.post(f"{FASTAPI_BASE_URL}{url}", json=data, headers=headers)
    return response


def get_user_info(user_id):
    # Define the base URL of your FastAPI auth-microservice
    FASTAPI_BASE_URL = "http://127.0.0.1:5000"

    response = requests.get(f"{FASTAPI_BASE_URL}/user/{user_id}")
    return response.json()