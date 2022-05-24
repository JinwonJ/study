from flask import jsonify

from core.bootstrap import Bootstrap
from modules.mail.globals import MAIL_SERVICES

api = Bootstrap.blueprint(__name__, '/mails/services')


@api.route('/', methods=['GET'])
def read_many():
    return jsonify(MAIL_SERVICES)
