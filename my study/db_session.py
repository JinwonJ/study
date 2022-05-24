from sqlalchemy import orm, inspect
from sqlalchemy.event.api import listen
from sqlalchemy.orm.session import Session as SessionBase, object_session


class SignallingSession(SessionBase):
    def __init__(self, **options):
        self._model_changes = {}
        self._attr_changes = {}
        SessionBase.__init__(self, **options)


class _SessionSignalEvents(object):
    """ 세션 이벤트 확장

    `after_insert`, `after_update`, `after_delete`는 `after_commit` 전 발생하여 모델을 참조할 수 없지만
    이를 기록 후 `after_commit` 이벤트 이후 실행하여 이 문제를 해결 한다.

    """

    def register(self):
        listen(SessionBase, 'after_commit', self._after_commit)
        listen(SessionBase, 'after_rollback', self._after_rollback)

    @staticmethod
    def _after_commit(session):
        if not isinstance(session, SignallingSession):
            return

        changes = session._model_changes

        if not changes:
            return

        for obj, change in changes.values():
            if hasattr(obj, 'on_changed_'):
                obj.on_changed_()

            if change == 'delete' and hasattr(obj, 'on_deleted_'):
                obj.on_deleted_()

            elif change == 'insert' and hasattr(obj, 'on_created_'):
                obj.on_created_()

            elif change == 'update' and hasattr(obj, 'on_updated_'):
                obj.on_updated_()

        changes.clear()

    @staticmethod
    def _after_rollback(session):
        if not isinstance(session, SignallingSession):
            return

        changes = session._model_changes
        if changes:
            changes.clear()


class _MapperSignalEvents(object):

    def __init__(self, mapper):
        self.mapper = mapper

    def register(self):
        mapper = self.mapper

        listen(mapper, 'before_update', self._before_update)
        listen(mapper, 'after_delete', self._after_delete)
        listen(mapper, 'after_insert', self._after_insert)
        listen(mapper, 'after_update', self._after_update)

    @staticmethod
    def _before_update(mapper, connection, target):
        session = object_session(target)
        state = inspect(target)

        changes = {}
        for attr in state.attrs:
            key = attr.key
            history = state.get_history(key, True)

            if not history.has_changes():
                continue

            changes[key] = history.added

        session._attr_changes = changes

    def _after_delete(self, mapper, connection, target):
        self._record(mapper, target, 'delete')

        if hasattr(target, 'on_delete_'):
            target.on_delete_()

    def _after_insert(self, mapper, connection, target):
        self._record(mapper, target, 'insert')

        if hasattr(target, 'on_insert_'):
            target.on_insert_()

    def _after_update(self, mapper, connection, target):
        session = object_session(target)

        self._record(mapper, target, 'update', session=session)

        if hasattr(target, 'on_update_'):
            target.on_update_(session._attr_changes)

    @staticmethod
    def _record(mapper, target, operation, **option):
        session = option.get('session')

        if not session:
            session = object_session(target)

        if isinstance(session, SignallingSession):
            pk = tuple(mapper.primary_key_from_instance(target))
            session._model_changes[pk] = (target, operation)


_MapperSignalEvents(orm.mapper).register()
_SessionSignalEvents().register()
