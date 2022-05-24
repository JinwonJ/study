from sqlalchemy import Column, String

from core.framework.model import Model, Extend, Timestamp, Seq


class MailTemplate(Model, Extend, Seq, Timestamp):
    __tablename__ = 'mail_templates'

    string_key_ = 'id'

    type = Column(String(50))
    id = Column(String(50), unique=True)
    descript = Column(String(200))
    descript_en = Column(String(200))
    subject = Column(String(200))
    subject_en = Column(String(200))
    body = Column(String(200))
    body_en = Column(String(200))



