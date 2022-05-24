import datetime
import re
from typing import List, Dict, Any, TypeVar, final

import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, func, String, Text, text, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base

from core.framework.exceptions import InvalidColumn, Required
from core.framework.service import use
from core.services.environment import Environment
from core.utils.imr import to_imr_camel
from core.utils.object import call_inherit_method, get_inherit_property
from core.utils.string import to_camel

Model = declarative_base()

environment = use(Environment)

# todo: Append All
NORMAL_TYPES = [
    Integer,
    String,
    Text
]

R = TypeVar('R')


def to_json(model_instance, **option):
    """ 모델을 JSON 형태로 변환
    """
    model = model_instance.__class__
    columns = model.__table__.columns

    excludes = option.get('excludes', [])

    if hasattr(model_instance, 'json_excludes_'):
        excludes += model.json_excludes_

    json_names = model.json_names_

    json = {}
    for column in columns:
        column_name = column.name
        if column_name in excludes or not hasattr(model_instance, column_name):
            continue

        value = getattr(model_instance, column_name)

        if isinstance(value, datetime.datetime):
            value = str(value)

        json_name = json_names[column_name]
        json[json_name] = value

    return json


class Extend:
    _relations: List[tuple] = None

    _related = None

    """변역 열 지원용 캐시"""
    _translates: Dict[str, List[str]] = {}

    """특수 형 캐시"""
    column_type_map_ = None

    """객체 해제형 캐시"""
    column_unpack_map_ = None

    priority_ = 0

    # JSON 속성명
    json_names_: Dict[str, str]

    def _exclude(self, target_column_names: List[str]):
        """ 열 제거

        :param target_column_names: 열 이름 배열
        :return:
        """
        for column in target_column_names:
            setattr(self, column, None)

        return self

    def _include(self, target_column_names: List[str]):
        """ 열 포함

        :param target_column_names: 열 이름 배열
        :return:
        """
        """
        columns = self.__table__.columns

        print(columns, target_column_names)

        for column in columns:
            column_name = column.name
            if column_name not in target_column_names:
                if hasattr(self, column_name) and getattr(self, column_name):
                   self.__setattr__(column_name, None)
        """
        return self

    def to_json(self, *except_column_name: str) -> Dict[str, Any]:
        """ `jsonify` 가능 형태로 변환

        - `timestamp` 열 자동 변환
        - 열이름 낙타법 변환: 예정
        - `getter` 자동 적용: 예정

        :return: 변경된 값
        """

        json = to_json(self)

        relations = self.__class__.get_relations_()

        for relation_name in relations:
            relation_model = getattr(self, relation_name)
            if relation_model:
                json_name = to_camel(relation_name)
                json[json_name] = to_json(relation_model)

        return json

    @classmethod
    def get_relations_(cls):
        if not cls._relations:
            result = {}

            relations = sqlalchemy.inspect(cls).relationships
            relation_models = []
            for rel in relations:
                relation_models.append(rel.mapper.class_)

            order = 0
            items = relations.items()
            for item in items:
                result.update({
                    item[0]: {
                        'property': item[1],
                        'model': relation_models[order]
                    }
                })

                order += 1

            cls._relations = result

        return cls._relations

    @classmethod
    def get_column_(cls, column_name: str) -> Column:
        """ 열 반환

        :return: 열
        """

        if not isinstance(column_name, str):
            return column_name

        column = cls.__getattribute__(cls, column_name)

        if not column:
            raise InvalidColumn(column_name)

        return column

    @classmethod
    def get_match_column_(cls, match_value, **option) -> Column:
        """ 검색 열 반환

        해당 값이 없을 때 모델에 정의된 `primary_key_` 값 사용

        :key match_column: 검색 열 이름
        :return: 열
        """
        match_column_name = option.get('match_column')

        if not match_column_name:
            if isinstance(match_value, str):
                match_column_name = get_inherit_property(cls, 'string_key_')

            elif isinstance(match_value, int):
                match_column_name = get_inherit_property(cls, '_int_key')

        if not match_column_name:
            match_column_name = get_inherit_property(cls, 'primary_key_')

        match_column = cls.__getattribute__(cls, match_column_name)

        return match_column

    def verify_(self, values: Dict[str, Any]):
        cls = self.__class__
        columns = cls.__table__.columns

        call_inherit_method(self, '_on_verify', values)

        ##############################
        # 번역 대상 열 자동 채움 처리
        translates = cls._translates
        for main_column_name in translates:
            if self.__getattribute__(main_column_name) is not None:
                continue

            language_column_names = translates[main_column_name]
            for language_column_name in language_column_names:
                value = self.__getattribute__(language_column_name)
                if value:
                    setattr(self, main_column_name, value)
                    break

        ##############################
        # 필수 열 검사
        for column in columns:
            name = column.name
            if column.nullable is False and column.autoincrement is not True:
                value = self.__getattribute__(name)
                if value is None:
                    raise Required(name)

        ##############################
        # 객체 해제 열 처리
        unpack_map = cls.column_unpack_map_
        for unpack_name in unpack_map:
            if unpack_name in values:
                value = values[unpack_name]

                if isinstance(value, dict):
                    setattr(self, unpack_name, value[unpack_map[unpack_name]])

        """
        try:
            # print(values)
            # print(self.to_json())

            call_inherit_method(self, 'on_verify', values)

            # print(self.to_json())

            for column in columns:
                name = column.name
                if column.nullable is False and column.autoincrement is not True:
                    value = self.__getattribute__(name)
                    if value is None:
                        raise KeyError(name)

        except ValueError as error:
            abort(400, description=f'{error} is invalid type')
        except KeyError as error:
            abort(400, description=f'{error} is required')
        except:
            print('Unknown Error')
        """
        """
        relations = cls._get_relations()
        for relations_property_name in relations:
            delattr(self, relations_property_name)
        """

    def _required(self, *column_names: str):
        """ 필수 열 값 확인

        :param column_names: 필수 열 이름
        :raise KeyError: 필수 값 누락 시 발생
        """
        for column_name in column_names:
            if not self.__getattribute__(column_name):
                raise Required(column_name)

    @classmethod
    @final
    def _on_load(cls):

        columns = cls.__table__.columns
        column_names = []
        column_type_map = {}
        column_unpack_map = {}

        json_names = {}
        for column in columns:
            name = column.name
            column_names.append(name)
            json_names.__setitem__(name, to_imr_camel(name))

            type_decorator = column.type.__class__
            type_name = type_decorator.__name__

            if hasattr(type_decorator, 'unpack'):
                column_unpack_map[name] = type_decorator.unpack

            if type_name not in column_type_map:
                column_type_map[type_name] = [column]
            else:
                column_type_map[type_name].append(column)

        setattr(cls, 'json_names_', json_names)
        setattr(cls, 'column_type_map_', column_type_map)
        setattr(cls, 'column_unpack_map_', column_unpack_map)

        ##############################
        # 번역 열 추출

        translates = {}
        for column_name in column_names:
            matched = re.search(r'_(kr|en)$', column_name)
            if not matched:
                continue

            language_suffix = matched.group(0)
            main_column_name = column_name[0:-len(language_suffix)]
            if not column_names.__contains__(main_column_name):
                continue

            if translates.get(main_column_name):
                translates[main_column_name].append(column_name)
            else:
                translates.__setitem__(main_column_name, [column_name])

        setattr(cls, '_translates', translates)

        """
        ##############################
        # 세션 이벤트 등록
        after_events = {
            'on_create_': [],
            'on_update_': [],
            'on_delete_': []
        }

        extend_classes = inspect.getmro(cls)

        for extend_class in extend_classes:
            members = inspect.getmembers(extend_class)
            for member in members:
                for event_name in after_events:
                    if member[0] == event_name and member[0]:
                        after_events[event_name].append(member[1])
                        break

        if len(after_events['on_create_']):
            @event.listens_for(cls, 'after_insert')
            def after_insert(model, connection, object):
                for callback in after_events['on_create_']:
                    callback(object)

        if len(after_events['on_update_']):
            @event.listens_for(cls, 'after_update')
            def after_update(model, connection, object):
                for callback in after_events['on_update_']:
                    callback(object)

        if len(after_events['on_delete_']):
            @event.listens_for(cls, 'after_delete')
            def after_delete(model, connection, object):
                for callback in after_events['on_delete_']:
                    callback(object)
        """


class Seq:
    """ `seq` 열 사용

    - 기본 `seq` 역순 정렬

    """
    primary_key_ = 'seq'
    sort_column_ = 'seq'
    sort_type_ = 'desc'

    seq = Column(Integer, primary_key=True, autoincrement=True)


class Inserted:
    """ `inserted`, 열 사용

    - 기본 `inserted` 역순 정렬
    - 갱신시 `updated` 변경

    """
    sort_column_ = 'inserted'
    sort_type_ = 'desc'

    inserted = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))


class Timestamp(Inserted):
    """ `inserted`, `updated` 열 사용

    - 기본 `inserted` 역순 정렬
    - 갱신시 `updated` 변경

    """

    updated = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=func.now())


class Icon:
    icon = Column(String(255))