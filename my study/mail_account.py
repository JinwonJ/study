from sqlalchemy import Column, Integer, String, DateTime, func, text

from core.framework.exceptions import InvalidType
from core.framework.model import Model, Extend, Timestamp, Seq
from modules.mail.globals import MAIL_SERVICE_DEFAULTS


class MailAccount(Model, Extend, Seq, Timestamp):
    __tablename__ = 'mail_accounts'

    json_excludes_ = [
        'password'
    ]

    service = Column(String(100), nullable=False)
    id = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    server = Column(String(255))
    port = Column(Integer)
    limit = Column(Integer)
    usage = Column(Integer, default=0, server_default=text('0'))
    sendtime = Column(DateTime(timezone=True), default=func.now(), server_default=text('CURRENT_TIMESTAMP'))

    def _on_verify(self, values):
        service = self.service

        if service not in MAIL_SERVICE_DEFAULTS:
            raise InvalidType('Service', service)

        # if service != 'standalone':
        #     self.required('id', 'password')

        defaults = MAIL_SERVICE_DEFAULTS[service]

        print(defaults)

        if not self.port:
            self.port = defaults['port']

        if not self.limit:
            self.limit = defaults['limit']
