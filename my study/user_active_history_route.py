from core.bootstrap import Bootstrap
from core.framework.service import use
from core.responses.list import response_list
from core.services.db import DB
from modules.user.models.user_active_history import UserActiveHistory

_db = use(DB)

api = Bootstrap.blueprint(__name__, '/users/actives')


@api.route('/histories', methods=['GET'])
def logging():
    return response_list(UserActiveHistory)
