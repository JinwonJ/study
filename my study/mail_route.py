from flask import jsonify, request

from core.bootstrap import Bootstrap
from core.framework.exceptions import Required
from core.framework.service import use
from core.services.db import DB
from modules.mail.models.mail_confirmer import MailConfirmer
from modules.mail.services.mail_service import MailService

api = Bootstrap.blueprint(__name__, '/mails')


@api.route('/', methods=['POST'])
def send():
    json = request.get_json()


    send = use(MailService).send(
        to=json.get('to'),
        subject=json.get('subject'),
        body=json.get('body'),
        template=json.get('template'),
        arguments=json.get('arguments')
    )

    return jsonify(send)


@api.route('/report', methods=['POST'])
def send_report():
    json = request.get_json()

    template_id = json.get('template')

    if not template_id:
        raise Required('template')

    _mail = use(MailService)

    template = _mail.get_template(template_id)

    db = use(DB)
    query = db.query(MailConfirmer, columns=[MailConfirmer.email])
    query = query.filter(MailConfirmer.reports.like('%|' + template_id + '|%'))

    items = query.all()

    # confirmer_address = ["jw@imrbiz.co.kr", "xfdu133@gmail.com"]
    confirmer_address = []
    #
    for item in items:
        confirmer_address.append(item[0])

    send = _mail.send(
        to=confirmer_address,
        template=template_id,
        arguments=json.get('arguments')

    )

    return jsonify(send)
