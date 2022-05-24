import os
import sys
from typing import List

import pandas as pd
from DateTime import DateTime
from sqlalchemy import inspect

from core.framework.model import Model
from core.framework.service import use
from core.framework.db_imports import engine
from core.imports.globals import TableService
from core.services.db import DB

_db = use(DB)

file_name = TableService


class make_csv():


    def table_to_csv():
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()

        for schema in schemas:
            if schema == 'public':

                print("schema: %s" % schema)
                table_list = []
                for table_name in inspector.get_table_names(schema=schema):
                    print(table_name)
                    table_list.append(table_name)
                print(table_list)
                return table_list

        '''
        This function creates a imports file from PostgreSQL with query
        '''

    def sql_query(talbe_list):

        for table in talbe_list:
            sql = 'Select * From '
            sql_make = sql + table
            file_path = 'C:/Users/jw/Desktop/table/'
            # file_modified_time = time.strftime("%Y%m%d%H%M%S")
            modified_time = str(os.path.getctime(file_path)).split('.')[0]

            # print(t)
            file_path_name = file_path + table + '#' + str(modified_time) + '.csv'

            try:
                conn = engine
                df = pd.read_sql(sql_make, conn)

                # df =df[df.columns.difference(['inserted', 'updated'])]
                # df = df['inserted'].isin([DateTime])
                # time = df.iloc[:,1:3]
                # df.loc[df['inseted'] == type(DateTime), 'inseted'] = 'now'
                df["updated"] ='now()'
                df["inserted"] ='now()'


                # Write to imports file
                df.to_csv(file_path_name, encoding='utf-8', header=True,
                          doublequote=True, sep=',', index=False)

                print("CSV File has been created")

            except Exception as e:
                print("Error: {}".format(str(e)))
                sys.exit(1)

    sql_query(table_to_csv())
