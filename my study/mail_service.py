import datetime
import re
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.framework.exceptions import InvalidType, Required
from core.framework.service import use, Usable
from core.services.db import DB
from modules.mail.globals import MAIL_SERVICE_DEFAULTS
from modules.mail.models.mail_account import MailAccount
from modules.mail.models.mail_template import MailTemplate

db = use(DB)


class MailService(Usable):
    """메일 발송자"""

    service_id_ = 'mail'

    def _on_built(self):
        query = db.query(MailAccount)
        accounts = query.all()

        all_accounts = []
        for c in accounts:
            all_accounts.append({'seq': c.seq, 'id': c.id, 'password': c.password, 'service': c.service,
                                 'port': c.port, 'usage': c.usage, 'sendtime': c.sendtime})

            sendtime = c.sendtime
            now = datetime.now()
            days = ((now - sendtime).days)

            if days == 0:
                c.usage = c.usage
            else:
                c.usage = 0

        query.session.commit()


    def get_account(self, need: int = 1):
        """ 사용 가능한 메일 계정 반환
        :param need: 필요한 수량
        :return:
        """
        return db.query(MailAccount).filter(
            MailAccount.usage + need < MailAccount.limit
        ).first()

    def get_server(self, account: MailAccount):

        common_service = MAIL_SERVICE_DEFAULTS.get(account.service)

        host = common_service.get('host')
        port = common_service.get('port')

        smtp_server = smtplib.SMTP(host=host, port=port)
        # SMTP인증이 필요하면 아래 주석을 해제하세요.
        # TLS(Transport Layer Security) 시작
        smtp_server.starttls()
        # 메일서버에 연결한 계정과 비밀번호
        smtp_server.login(account.id, account.password)

        return smtp_server

    def get_template(self, id: str):
        """ 템플릿 아이디로 템플릿 반환
        :return:
        """
        template = db.one(MailTemplate, id)

        if not template:
            raise InvalidType('Template ID', id)
        return template

    def send(self, to=None, subject: str = None, body: str = None, **option) -> bool:
        """ 메일 발송

        :description:

            ```python
            mail = use(MailService)

            mail.send('jw@imrbiz.co.kr', '제목', '본문')
            mail.send(['jw@imrbiz.co.kr'], '제목', '본문')

            mail.send(
                to='imrbiz.co.kr',
                subject='제목',
                body='본문'
            )

            mail.send(**{
                'to': 'jw@imrbiz.co.kr',
                'subject': '제목',
                'body': '본문'
            })
            ```

        :param to: 수신자
        :param subject: 제목
        :param body: 본문
        :key to: 수신자
        :key subject: 제목
        :key body: 본문
        :key template: 템플릿 아이디
        :key arguments: 템플릿 변수
        :return:
        """

        to = option.get('to', to)
        subject = option.get('subject', subject)
        body = option.get('body', body)
        template_id = option.get('template')
        if not to:
            raise Required('to')

        if template_id:
            template = self.get_template(template_id)

            if not template:
                raise InvalidType('Template ID', template_id)

            subject = template.subject
            body = template.body

            arguments = option.get('arguments')

            if not isinstance(arguments, dict):
                raise InvalidType('Arguments', arguments)

            if arguments:
                for name in arguments:
                    value = arguments.get(name)
                    body = re.sub(
                        re.compile(r'{{\s*' + name + '\s*}}'),
                        value,
                        body
                    )

        else:
            if not subject:
                raise Required('subject')

            if not body:
                raise Required('body')

        if isinstance(to, str):
            to = to.split(',')

        need = len(to)

        account = self.get_account(need)

        if not account:
            return False

        server = self.get_server(account)

        if not server:
            return False

        from_address = account.id

        # to_address = []
        # for to1 in to:
        #     to_address.append({
        #         'to': to1
        #     })

        # html_body = MIMEText(body, 'html')
        mime_body = MIMEText(body)

        content = MIMEMultipart()
        # content['From'] = from_address
        # content['To'] = to_address
        content['Subject'] = subject
        content.attach(mime_body)

        send = server.send_message(
            content,
            to_addrs=to,
            from_addr=from_address
        )
        account.usage += need
        account.sendtime = datetime.now()

        session = db.session
        session.merge(account)
        session.commit()

        #
        # if send:
        #     account.usage += need
        #     account.sendtime = datetime.now()
        #     db.session.commit()
        #     print(account.usage)
        #     print(account.sendtime)

        return send
