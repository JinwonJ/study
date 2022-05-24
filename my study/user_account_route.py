from flask import request
from sqlalchemy import text
from werkzeug.exceptions import Unauthorized

from core.bootstrap import Bootstrap
from core.framework.exceptions import Required
from core.framework.service import use
from core.responses.create import response_create
# from core.responses.create import response_create
from core.responses.delete_any import response_delete_any
from core.responses.functional_path import response_functional_path
from core.responses.list import response_list
from core.responses.read import response_read
from core.responses.update import response_update
from modules.user.models.user_account import UserAccount
from modules.user.services.user_account_service import UserAccountService
from modules.user.services.user_permission_service import UserPermissionService
from modules.user.services.user_service import UserService

api = Bootstrap.blueprint(__name__, '/users/accounts')


@api.route('/', methods=['POST'])
# @permit('user/account/write')
def create():
    return response_create(UserAccount)


@api.route('/', methods=['GET'])
# @permit('users/accounts/read')
def read_many():
    return response_list(UserAccount)


@api.route('/<int:seq>', methods=['GET'])
# @permit('users/accounts/read')
def read(seq: int):
    return response_read(UserAccount, seq, joins=True)


@api.route('/<int:seq>', methods=['PATCH'])
def update(seq: int):
    logger = use(UserService).get_logger()

    if logger is None:
        raise Unauthorized()

    if logger['seq'] != seq:
        if not use(UserPermissionService).permit('user/account/write'):
            raise Unauthorized()

    body = request.get_json()

    new_password = body.get('newPassword')
    if new_password:
        password = body.get('password')
        if not password:
            raise Required('password')

        # Check the Logger's Password. Not with Account Password.
        if not use(UserAccountService).check_password(logger['id'], password):
            raise Unauthorized('Invalid Password')

        body['password'] = body['newPassword']
        body['passwordChanged'] = text('CURRENT_TIMESTAMP')
        body.__delitem__('newPassword')

    return response_update(UserAccount, seq, body=body)


@api.route('/', methods=['DELETE'])
@api.route('/<seq>', methods=['DELETE'])
# @permit('users/accounts/delete')
def delete(seq=None):
    return response_delete_any(UserAccount, seq)


@api.route('/<string:plural_column_name>/<string:method_name>', methods=['GET', 'POST'])
@api.route('/<string:plural_column_name>/<string:method_name>/<string:method_value>', methods=['GET'])
def functional_path(plural_column_name: str, method_name: str, method_value: str = None):
    return response_functional_path(UserAccount, plural_column_name, method_name, method_value)
