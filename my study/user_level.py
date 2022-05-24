from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.orm import synonym

from core.framework.model import Model, Extend, Timestamp, Seq


class UserLevel(Model, Extend, Timestamp, Seq):
    __tablename__ = 'user_levels'
    id = Column(Integer, unique=True, nullable=False)
    name = Column(String(150))
    name_en = Column(String(150))

    ##############################
    # PERMISSIONS

    _permissions = Column('permissions', TEXT)

    @property
    def permissions(self):
        if self._permissions:
            return self._permissions.split(',')
        return []

    @permissions.setter
    def permissions(self, value):
        if isinstance(value, list):
            value = ','.join(value)
        self._permissions = value

    permissions = synonym('_permissions', descriptor=permissions)