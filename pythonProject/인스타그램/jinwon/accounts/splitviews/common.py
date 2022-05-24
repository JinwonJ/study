# common.py
import string
import random
import hashlib
import base64
from django.contrib.auth.hashers import pbkdf2

def hashing_password(user_pw):
    # salt 생성 - salt는 최소 128bit 이상이 권고된다 하여 다음과 같이 생성
    count = random.randint(16, 21)
    string_pool = string.ascii_letters + string.digits + string.punctuation
    salt = "".join(random.choices(string_pool, k=count))    # count만큼 문자열을 랜덤 선택하여 합치기

    hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
    hashed_pw = base64.b64encode(hash).decode('ascii').strip()

    return salt, hashed_pw