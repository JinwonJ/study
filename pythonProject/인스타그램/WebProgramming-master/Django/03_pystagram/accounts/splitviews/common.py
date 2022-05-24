from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.contrib import messages
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import os
import re
import uuid
import string
import random
import hashlib
import base64
from django.contrib.auth.hashers import pbkdf2
from django.core.files.storage import default_storage


def hashing_password(user_pw):
    count = random.randint(16, 21)
    string_pool = string.ascii_letters + string.digits + string.punctuation
    salt = "".join(random.choices(string_pool, k=count))

    hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
    hashed_pw = base64.b64encode(hash).decode('ascii').strip()

    return salt, hashed_pw


def profileImageFileUpload(user, profileImg):
    fileName, extension = os.path.splitext(profileImg.name)

    newFileName = str(uuid.uuid4()) + extension
    filePath = os.path.join('image', user.username, 'profile', newFileName)

    default_storage.save(filePath, profileImg)
    profile_img_url = default_storage.url(filePath)

    return profile_img_url


def profileImageFileDelete(profile_img_src):
    tmp_path = re.findall(r'image.*', profile_img_src)
    delete_path = tmp_path[0]

    default_storage.delete(delete_path)