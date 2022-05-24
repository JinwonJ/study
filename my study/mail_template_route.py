from core.bootstrap import Bootstrap
from core.responses.create import response_create
from core.responses.delete import response_delete
from core.responses.functional_path import response_functional_path
from core.responses.list import response_list
from core.responses.update import response_update

from modules.mail.models.mail_template import MailTemplate

api = Bootstrap.blueprint(__name__, '/mails/templates')


@api.route('/', methods=['POST'])
def create():
    return response_create(MailTemplate)


@api.route('/', methods=['GET'])
def read_many():
    return response_list(MailTemplate)


@api.route('/<int:seq>', methods=['GET'])
def read(seq: int):
    return response_list(MailTemplate, seq)


@api.route('/<int:seq>', methods=['PATCH'])
def update(seq: int):
    return response_update(MailTemplate, seq)


@api.route('/<int:seq>', methods=['DELETE'])
def delete(seq: int):
    return response_delete(MailTemplate, seq)


@api.route('/<string:plural_column_name>/<string:method_name>', methods=['GET', 'POST'])
@api.route('/<string:plural_column_name>/<string:method_name>/<string:method_value>', methods=['GET'])
def functional_path(plural_column_name: str, method_name: str, method_value: str = None):
    return response_functional_path(MailTemplate, plural_column_name, method_name, method_value)
