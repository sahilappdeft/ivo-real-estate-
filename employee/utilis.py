import secrets
import string

from django.conf import settings

base_url = settings.BASE_URL

def generate_token(id, length=20):
    alphabet = string.ascii_letters + string.digits
    # Combine email and a random string to create the token
    random_part = ''.join(secrets.choice(alphabet) for _ in range(length))
    return f"{id}-{random_part}"


def generate_token_link(token):
    return f"{base_url}api/auth/setup-account/?token={token}"
