from core.bootstrap import Bootstrap
from core.responses.create import response_create
from core.responses.delete import response_delete
from core.responses.delete_all import response_delete_all
from core.responses.delete_any import response_delete_any
from core.responses.functional_path import response_functional_path
from core.responses.list import response_list
from core.responses.read import response_read
from core.responses.update import response_update
from modules.mail.models.mail_account import MailAccount

api = Bootstrap.blueprint(__name__, '/mails/accounts')


@api.route('/', methods=['POST'])
def create():
    return response_create(MailAccount)


@api.route('/', methods=['GET'])
def read_many():
    return response_list(MailAccount)


@api.route('/<int:seq>', methods=['GET'])
def read(seq):
    return response_read(MailAccount, seq)


@api.route('/<int:seq>', methods=['PATCH'])
def update(seq):
    return response_update(MailAccount, seq)


@api.route('/', methods=['DELETE'])
@api.route('/<seq>', methods=['DELETE'])
def delete(seq=None):
    return response_delete_any(MailAccount, seq)


@api.route('/<string:plural_column_name>/<string:method_name>', methods=['GET', 'POST'])
@api.route('/<string:plural_column_name>/<string:method_name>/<string:method_value>', methods=['GET'])
def functional_path(plural_column_name: str, method_name: str, method_value: str = None):
    return response_functional_path(MailAccount, plural_column_name, method_name, method_value)
