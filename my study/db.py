from typing import TypeVar, Dict, Any, Callable, List, Tuple, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Query, defer, contains_eager, load_only, Session

from core.framework.db_session import SignallingSession
from core.framework.exceptions import InvalidItem
from core.framework.model import Extend, Model
from core.framework.service import Usable, use
from core.responses.search_string_paginate import search_string_limit
from core.responses.search_string_query import search_string_query
from core.responses.search_string_sort import search_string_sort
from core.services.environment import Environment
from core.utils.imr import to_imr_snake
from core.utils.object import call_inherit_method

environment = use(Environment)

R = TypeVar('R')


class DB(Usable):
    """
    Database Service
    """
    # session: scoped_session = None
    engine = None

    @property
    def session(self) -> Session:
        session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=SignallingSession
        )

        session = scoped_session(session)
        # session.expire_on_commit = False

        return session

    def connect(self, id: str, password: str, name: str, **options):
        """ 데이터베이스 연결
        """

        sql = options.get('type', 'postgresql')

        protocols = {
            'pg': 'postgresql+psycopg2',
            'postgre': 'postgresql+psycopg2',
            'postgresql': 'postgresql+psycopg2'
        }

        protocol = protocols[sql]

        if protocol is None:
            raise Exception(sql + ' is not supported sql type')

        host = options.get('host', 'localhost')
        port = options.get('port')

        encoding = options.get('encoding', 'utf8')
        pool_size = options.get('pool_size', 100)
        max_overflow = options.get('pool_size', 100)

        if port is None:
            # if protocol is 'postgresql' :
            port = 5432

        dsn = f'{protocol}://{id}:{password}@{host}:{port}/{name}'

        engine = create_engine(dsn, client_encoding=encoding, pool_size=pool_size, max_overflow=max_overflow)
        self.engine = engine

        return self

    def disconnect(self):
        # todo: 데이터베이스 연결 종료 구현
        return self

    def create_table(self):
        """ 테이블 생성
        """
        if self.engine is None:
            raise Exception('Does not connected Database')

        self._debug('Create Tables')
        Model.metadata.create_all(bind=self.engine)

        return self

    def query(self, model: Callable[[Extend], R], match_value=None, **option) -> Query:
        """ 쿼리 생성

        `db.session.query(Model)` 축약

        :param model: 모델
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key matches: 다중 일치 대상 조건 설정
        :key columns: 반환 컬럼 설정
        :key joins: 조인 맵 설정
          {
            join_column_name: [joined_model_column_name]
          }
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정
        :return: 데이터베이스 쿼리
        """

        if environment.print_query_option:
            print(option)

        session = option.get('session')

        if not session:
            session = self.session

        joins = option.get('joins')
        columns = option.get('columns', [model])

        if joins:
            if isinstance(joins, bool) and joins:
                joins = getattr(model, 'join_')

            relation_properties = []
            query_option = []

            relations = model.get_relations_()

            # load_columns = [*cls.__table__.target_column_names]

            if isinstance(joins, dict):
                for join_property_name in joins:
                    join_column_names = joins[join_property_name]

                    relation_property = getattr(model, join_property_name)
                    relation_properties.append(relation_property)

                    relation = relations[join_property_name]
                    relation_model = relation['model']
                    relation_columns = relation_model.__table__.columns

                    # tables.append(relation_model)

                    deffer_columns = []
                    load_column_names = []
                    for relation_column in relation_columns:
                        relation_column_name = relation_column.name
                        if relation_column_name not in join_column_names:
                            deffer_columns.append(
                                defer(relation_column_name)
                            )

                        else:
                            load_column_names.append(relation_column_name)
                            # load_columns.append(relation_column)

                    # query_option.append(*deffer_columns)
                    query_option.append(
                        contains_eager(relation_property).options(
                            *deffer_columns,
                            load_only(*load_column_names),
                        )
                    )

            query = session.query(*columns)

            for relation_property in relation_properties:
                query = query.join(relation_property)
            query = query.options(*query_option)

        else:
            query = session.query(*columns)

        if match_value:
            match_column = model.get_match_column_(match_value, **option)
            if isinstance(match_value, list):
                query = query.filter(match_column.in_(match_value))
            else:
                query = query.filter(match_column == match_value)

        matches = option.get('matches')
        if matches:
            equals = []
            for match_column_name in matches:
                match_column = model.get_column_(match_column_name)
                equals.append(match_column == matches[match_column_name])
            query = query.filter(*equals)

        (query, queried) = search_string_sort(model, query, **option)
        (query, queried) = search_string_query(model, query, **option)

        """
        if joins:
            if isinstance(joins, dict):
                for item in items:
                    for join_property_name in joins:
                        fixed_join_property = {}
                        child_property = getattr(item, join_property_name)
                        for child_column_name in joins[join_property_name]:
                            fixed_join_property.update({
                                child_column_name: getattr(child_property, child_column_name)
                            })

                        setattr(item, join_property_name, fixed_join_property)

            else:
                for item in items:
                    for join_column_name in joins:
                        setattr(
                            item,
                            join_column_name,
                            item.__getattribute__(join_column_name)
                        )
        """

        if environment.print_sql:
            print(str(query).replace(',', ',\n'))

        return query

    def create(self, model: Callable[[Extend], R], values: Dict[str, Any], **option) -> (Session, R):
        """ 모델 추가

        `db.session.add(Model)` 축약

        :param model: 모델
        :param values: 생성 값
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 추가될 모델
        """

        session = option.get('session')

        if not session:
            session = self.session

        snake_values = {}
        for camelcase_name in values:
            value = values[camelcase_name]
            if not isinstance(value, dict):
                snake_values.__setitem__(to_imr_snake(camelcase_name), value)

        new_item = model(**snake_values)

        new_item.verify_(values)

        call_inherit_method(new_item, '_on_create')

        session.add(new_item)

        return session, new_item

    def update(self, model: Callable[[Extend], R], values: Dict[str, Any], match_value, **option) -> (Session, R):
        """ 모델 갱신 대기

        :param model: 모델
        :param values: 수정 값
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return:
        """

        session = option.get('session')

        if not session:
            session = self.session
            option.update({'session': session})

        item = self.one(model, match_value, **option)

        if not item:
            # raise ValueError('Cannot Find Item')
            raise InvalidItem()

        for value_name in values:
            snake_name = to_imr_snake(value_name)
            new_value = values[value_name]
            try:
                item.__setattr__(snake_name, new_value)
            except:
                pass

        call_inherit_method(item, '_on_update')
        item.verify_(values)

        return session, item

    def delete(self, model: Callable[[Extend], R], match_value, **option
               ) -> Union[Tuple[Session, R], Tuple[Session, List[R]]]:
        """ 모델 삭제

        `session.delete(Model)`

        :param model: 모델
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 삭제될 모델
        """

        session = option.get('session')

        if not session:
            session = self.session

        match_value_type = type(match_value)

        if match_value_type == int:
            item = self.one(model, match_value, **option)

            if item:
                item = session.merge(item)
                session.delete(item)
            return session, item

        if isinstance(match_value, str):
            match_value = match_value.split(',')

        if isinstance(match_value, list):
            match_column = model.get_match_column_(match_value, **option)

            query = self.query(model).filter(match_column.in_(match_value))
            items = query.all()

            if items:
                session = self.session
                for item in items:
                    item = session.merge(item)
                    session.delete(item)

            return session, items

    def delete_all(self, model: Callable[[Extend], R], **option) -> int:
        """ 전체 삭제

        `Query.delete()`

        :param model: 모델
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 삭제될 수량
        """

        option.__setitem__('sort', False)

        return self.query(model, **option).delete()

    def replace(self, model: Callable[[Extend], R], values: Dict, match_value=None, **option) -> (Session, R):
        """ 모델 생성 또는 갱신

        :param model: 모델
        :param values: 수정 값
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return:
        """

        session = option.get('session')

        if not session:
            session = self.session
            option.update({'session': session})

        item = self.one(model, match_value, **option)

        if item:
            for name in values:
                item.__setattr__(name, values.get(name))
        else:
            item = model(**values)
            item.verify_(values)
            session.add(item)

        return session, item

    def created(self, model: Callable[[Extend], R], values: dict, **option) -> R:
        """ 모델 추가 적용

        ```python
        session.add(Model)
        session.commit()
        ```

        :param model: 모델
        :param values: 생성 값
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 추가된 모델
        """
        session, new_item = self.create(model, values, **option)
        session.commit()

        # occurred error about model have lost session before lazy loading in some environment.
        # auto close after commit option was not work
        session.refresh(new_item)

        return new_item

    def updated(self, model: Callable[[Extend], R], values: Dict[str, Any], match_value, **option) -> R:
        """ 모델 갱신 처리

        :param model: 모델
        :param values: 수정 값
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return:
        """

        session, new_item = self.update(model, values, match_value, **option)
        session.commit()
        session.refresh(new_item)

        return new_item

    def deleted(self, model: Callable[[Extend], R], match_value, **option) -> R:
        """ 모델 삭제 적용

        ```python
        session.delete(Model)
        session.commit()
        ```

        :param model: 모델
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 삭제된 모델 수
        """

        session, item = self.delete(model, match_value, **option)
        session.commit()

        return item

    def deleted_all(self, model: Callable[[Extend], R], **option) -> int:
        """ 전체 삭제 적용

        ```python
        Query.delete()
        session.commit()
        ```

        :param model: 모델
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 삭제된 수량
        """

        session = option.get('session')
        if not session:
            session = self.session
            option.update({'session': session})

        count = self.delete_all(model, **option)
        session.commit()

        return count

    def replaced(self, model: Callable[[Extend], R], values: Dict, match_value=None, **option) -> R:
        session, item = self.replace(model, values, match_value, **option)
        session.commit()

        return item

    def all(self, model: Callable[[Extend], R], match_value=None, **option) -> List[R]:
        """ 전체 행 반환

       `db.session.query(Model).all()` 축약

        :param model: 모델
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key columns: 반환 컬럼 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return:
        """
        return self.query(model, match_value, **option).all()

    def one(self, model: Callable[[Extend], R], match_value=None, **option) -> R:
        """ 단일 읽기


        :param model: 모델
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정

        :return: 읽은 모델
        """

        query = self.query(model, match_value, **option)
        item = query.first()

        # Todo: to_json 에서 자동화 되므로 필요성 확인 필요
        if item:
            except_columns = option.get('except_columns')
            if except_columns:
                item._exclude(except_columns)

            return item

        return None

    def list(self, model: Callable[[Extend], R], match_value=None, **option) -> (Query, int):
        """ 목록 읽기

        :param model: 모델
        :param match_value: 일치 조건 설정
            - 일치 대상이 숫자 일 때 `_int_key` > `primary_key_` 사용
            - 일치 대상이 문자 일 때 `string_key_` > `primary_key_` 사용
        :key match_column: 일치 대상 열 설정
        :key joins: 조인 맵 설정
        :key query: 검색(등급2) 설정
        :key keyword: 검색(등급1) 검색어 설정
        :key target: 검색(등급1) 대상 설정
        :key sort: 정렬 설정
        :key limit: 반환 수량 제한
        :key page: 반환 수량 제한 쪽

        :return:
        """

        query = self.query(model, match_value, **option)

        count = query.count()

        (query, queried) = search_string_limit(model, query, **option)

        return query, count
