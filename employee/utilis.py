import secrets
import string

def generate_token(id, length=20):
    alphabet = string.ascii_letters + string.digits
    # Combine email and a random string to create the token
    random_part = ''.join(secrets.choice(alphabet) for _ in range(length))
    return f"{id}-{random_part}"
