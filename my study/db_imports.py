from os.path import basename, dirname
from typing import List

import numpy as np

from core.framework.model import Model
from core.framework.service import use
from core.services.db import DB
from core.utils.string import to_camel, to_capital

_db = use(DB)

import os

import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('postgresql+psycopg2://postgres:9203@localhost:5432/p2220', convert_unicode=False,
                       client_encoding='utf8',
                       pool_size=700, max_overflow=700)



# engine = create_engine(
#     dsn,
#     components = 'port',
#     convert_unicode=False,
#     client_encoding='utf8',
#     pool_size=700, max_overflow=700
# )

def db_imports(files: List[str]):


    models = [
        mapper.class_
        for mapper in Model.registry.mappers
    ]


    targets = []

    for file in files:
        file_modified_time = str(os.path.getmtime(file)).split('.')[0]

        if '#' in file:
            flagged_name = file.split('#')
            name = basename(flagged_name[0])
            flagged_modified_time = flagged_name[1]

            if flagged_modified_time.endswith('.csv'):
                flagged_modified_time = flagged_modified_time[0:-4]


            # 파일 수정 시간과 파일명의 기록 시간이 같으면 이미 등록한 파일
            # 파일명은 수정해도 수정시간이 변하지 않음
            if file_modified_time == flagged_modified_time:
                _db.debug_(f'{name} was imported already')
                continue
        else:
            name = basename(file)[:-4]

        target_name = to_capital(to_camel(name))

        not_found = True

        for model in models:
            if target_name == model.__name__:

                not_found = False
                targets.append((file, name, model, file_modified_time))
                break

        if not_found:
            raise IOError(f'{name} is not supported model')

    # 모델 설정에 의한 정렬
    targets.sort(key=lambda target: -target[2].priority_)

    for file, name, model, file_modified_time in targets:
        _db.warn_(name)

        df = pd.read_csv(file, index_col=0)

        df.to_sql(model.__tablename__,
                  engine,
                  if_exists='append',
                  index = False)
        # 파일명 변경
        flagged_name = os.path.join(dirname(file), name + '#' + file_modified_time + '.csv')
        os.rename(file, flagged_name)

    file_list = os.listdir('./imports')
    if '#' in file_list:
        flagged_name = file_list.split('#')
        name = basename(flagged_name[0])
        flagged_modified_time = flagged_name[1]

        if flagged_modified_time.endswith('.csv'):
            flagged_modified_time = flagged_modified_time[0:-4]

        # 파일명 변경
    # flagged_name = os.path.join(dirname(file), name + '#' + file_modified_time + '.csv')
    # print(flagged_name)
    # os.rename(file, flagged_name)






