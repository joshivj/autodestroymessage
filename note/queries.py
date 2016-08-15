import random
import string
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

def create_random_key():
    """
    Return a random string of 32 characters
    :return:
    """
    SIZE = 32
    random_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(SIZE)])
    return random_key

#Encryption/Description functions
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(message))

def decrypt(ciphertext, key):
    enc = base64.b64decode(ciphertext)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(enc[AES.block_size:])
    return plaintext.rstrip(b"\0")

#Hash function

def create_hashkey(key):
    """
    Returns Hash the key, and return HashedNoteID.
    :param key:
    :return:
    """
    return hashlib.md5(key).hexdigest()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip