from core.bootstrap import Bootstrap
from modules.mail.models.mail_account import MailAccount
from modules.mail.models.mail_confirmer import MailConfirmer
from modules.mail.models.mail_template import MailTemplate
from modules.mail.services.mail_service import MailService

""" 모델 수출
:description:
    - 테이블 생성
"""
export_models = [
    MailAccount,
    MailConfirmer,
    MailTemplate
]

""" 서비스 수출
:description:
    - 서비스 초기화
    - 대리 서비스 연동
"""
export_services = [
    MailService
]
