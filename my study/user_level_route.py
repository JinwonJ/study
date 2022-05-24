from core.bootstrap import Bootstrap
from core.responses.create import response_create
from core.responses.delete_any import response_delete_any
from core.responses.functional_path import response_functional_path
from core.responses.list import response_list
from core.responses.read import response_read
from core.responses.update import response_update
from modules.user.models.user_level import UserLevel

api = Bootstrap.blueprint(__name__, '/users/levels')


@api.route('/', methods=['POST'])
def create():
    return response_create(UserLevel)


@api.route('/', methods=['GET'])
def read_many():
    return response_list(UserLevel)


@api.route('/<int:seq>', methods=['GET'])
def read(seq):
    return response_read(UserLevel, seq)


@api.route('/<int:seq>', methods=['PATCH'])
def update(seq):
    return response_update(UserLevel, seq)


@api.route('/', methods=['DELETE'])
@api.route('/<seq>', methods=['DELETE'])
def delete(seq=None):
    return response_delete_any(UserLevel, seq)


@api.route('/<string:plural_column_name>/<string:method_name>', methods=['GET', 'POST'])
@api.route('/<string:plural_column_name>/<string:method_name>/<string:method_value>', methods=['GET'])
def functional_path(plural_column_name: str, method_name: str, method_value: str = None):
    return response_functional_path(UserLevel, plural_column_name, method_name, method_value)
