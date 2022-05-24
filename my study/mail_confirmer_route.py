from core.bootstrap import Bootstrap
from core.responses.create import response_create
from core.responses.delete import response_delete
from core.responses.functional_path import response_functional_path
from core.responses.list import response_list
from core.responses.read import response_read
from core.responses.update import response_update

from modules.mail.models.mail_confirmer import MailConfirmer

api = Bootstrap.blueprint(__name__, '/mails/confirmers')


@api.route('/', methods=['POST'])
def create():
    return response_create(MailConfirmer)


@api.route('/', methods=['GET'])
def read_many():
    return response_list(MailConfirmer)


@api.route('/<int:seq>', methods=['GET'])
def read(seq: int):
    return response_read(MailConfirmer, seq)


@api.route('/<int:seq>', methods=['PATCH'])
def update(seq):
    return response_update(MailConfirmer, seq)


@api.route('/<int:seq>', methods=['DELETE'])
def delete(seq):
    return response_delete(MailConfirmer, seq)


@api.route('/<string:plural_column_name>/<string:method_name>', methods=['GET', 'POST'])
def functional_path(plural_column_name: str, method_name: str):
    return response_functional_path(MailConfirmer, plural_column_name, method_name)
