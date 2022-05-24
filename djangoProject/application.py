
import requests
from flask import *

# class token_get_toss():
#
def call_token():
    application_headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "username": "test",
        "password": "test"
    }
    jsonS = json.dumps(data)

    token_auth = requests.post("http://localhost:8081/auth/token", headers=application_headers, data=jsonS).headers[
        "Authorization"]

    token_headers = {'Content-Type': 'application/json; charset=utf-8', "Authorization": token_auth}
    print(token_headers["Authorization"])
    token_toss = requests.post("http://localhost:5000/auth", headers=token_headers, data=jsonS)
    print(token_toss.text)


call_token()