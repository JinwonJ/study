from sqlalchemy import Column, String, TEXT
from sqlalchemy.orm import synonym

from core.framework.model import Model, Extend, Timestamp, Seq
from core.utils.list import to_wrap
from core.utils.string import to_unwrap


class MailConfirmer(Model, Extend, Seq, Timestamp):
    __tablename__ = 'mail_confirmers'

    email = Column(String(50), unique=True, nullable=False)

    _reports = Column('reports', TEXT)

    @property
    def reports(self):
        if self._reports:
            return to_unwrap(self._reports)
        return []

    @reports.setter
    def reports(self, value):
        if isinstance(value, list):
            value = to_wrap(value)
        self._reports = value

    reports = synonym('_reports', descriptor=reports)