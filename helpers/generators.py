import random
import string

def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase, k=10))
    domain = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"{username}@{domain}.com"

def generate_random_name():
    return ''.join(random.choices(string.ascii_letters, k=10))

def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))