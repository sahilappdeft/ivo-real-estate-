import requests

# Success middleware
def success(message, data):
    res = {
        'success': True,
        'message': message,
        'data': data,
    }
    return res


# Error middleware
def error(message, data):
    res = {
        'success': False,
        'message': message,
        'data': data,
    }
    return res

def call_auth_microservice(url, data, token=None):
    # Define the base URL of your FastAPI auth-microservice
    FASTAPI_BASE_URL = "http://127.0.0.1:5000"

     # Define the headers with the token
    headers = {'Authorization': f'Bearer {token}'}
    if not token:
        headers = {}

    response = requests.post(f"{FASTAPI_BASE_URL}{url}", json=data, headers=headers)
    return response
