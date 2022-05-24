import flask
import requests
from flask import *
from flask_jwt_extended import *

# request_headers = {'Content-Type': 'application/json; charset=utf-8'}
#
# token_auth = requests.post("http://localhost:8081/auth/token", headers=request_headers, data=jsonS).headers[
#     "Authorization"]

app = Flask(import_name=__name__)
app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="IMR"
)
jwt = JWTManager(app)


data = {
    "username": "test",
    "password": "test"
}
jsonS = json.dumps(data)


@app.route("/auth", methods=['POST'])
def resource_sever():

    POST_request = request.headers['Authorization']

    print(POST_request)

    request_headers_check = {'Content-Type': 'application/json; charset=utf-8', "Authorization": POST_request}

    print(request_headers_check['Authorization'])
    Test_value = request_headers_check['Authorization']
    check_token = requests.post("http://localhost:8081/auth/access_token_info", headers=request_headers_check, data=jsonS)


    if check_token.status_code == 200:
        # if POST_request == Test_value():
        print(request.headers['Authorization'])
        print("pass")
        return "test return"
    else:
        print("check plz")
        abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
