import os
import uuid
import datetime
import json

from accounts.models import User
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage


def fileUpload(user, postImg):
    fileName, extension = os.path.splitext(postImg.name)

    newFileName = str(uuid.uuid4()) + extension
    filePath = os.path.join('image', user.username, newFileName)

    default_storage.save(filePath, postImg)
    post_img_url = default_storage.url(filePath)

    return post_img_url