from flask import jsonify
from werkzeug.exceptions import Unauthorized

from core.bootstrap import Bootstrap
from core.framework.service import use
from core.services.db import DB
from core.utils.request import get_body, Valid
from modules.user.models.user_account import UserAccount
from modules.user.services.user_account_service import UserAccountService
from modules.user.services.user_service import UserService

_db = use(DB)
api = Bootstrap.blueprint(__name__, '/users')


@api.route('/login', methods=["POST"])
def login():
    body = get_body({
        'id': Valid(str, required=True),
        'password': Valid(str, required=True),
    })

    id_ = body['id']
    password = body['password']

    account = _db.one(UserAccount, id_)

    if account is None:
        raise Unauthorized()

    if not use(UserAccountService).check_password(account, password):
        raise Unauthorized()

    use(UserService).set_logger(account)

    return jsonify(account.to_json())


@api.route('/login/restore', methods=['POST'])
def restore():
    body = get_body({
        'id': Valid(str, required=True)
    })

    logger = use(UserService).get_logger()

    if logger and body['id'] == logger['id']:
        return logger

    return jsonify(False)


@api.route('/logout', methods=['GET', 'POST'])
def logout():
    use(UserService).logout()

    return '', 200

@api.route('/find-group_id', methods=["POST"])
def find_id():
    body = get_body({
        'email': Valid(str, required=True)
    })

    account = _db.one(UserAccount, matches={'email': body['email']})

    if account:
        return jsonify(account.id)
    else:
        return jsonify(None)


@api.route('/reset-password', methods=["POST"])
def reset_password():
    body = get_body({
        'id': Valid(str, required=True),
        'email': Valid(str, required=True),
    })

    account = _db.one(
        UserAccount,
        matches={
            'id': body['id'],
            'email': body['email']
        }
    )

    if account:
        # todo: Send randomized password to email
        account.password = 'imr'
        account.passwordChanged = None

        session = _db.session
        session.merge(account)
        session.commit()

    return '', 200


@api.route('/register', methods=["POST"])
def register():
    pass
