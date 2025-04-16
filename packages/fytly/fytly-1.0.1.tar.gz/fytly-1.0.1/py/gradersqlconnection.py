from sqlalchemy import  create_engine

import os


from py.graderconfigs import GraderConfigs
grader_configs = GraderConfigs()
username=grader_configs.props.get('username')
password = grader_configs.props.get('password')
host=grader_configs.props.get('host')
port=grader_configs.props.get('port')





class GraderMySQLConnection:


    _instance = None

    def __init__(self):
        self.database_url=f'mysql+pymysql://{username}:{password}@{host}:{port}'
        self._sql_connection='None'

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    @classmethod
    def get_mysqlconnection(self):
        database_url = f'mysql+pymysql://{username}:{password}@{host}:{port}'
        print(database_url)
        _engine = create_engine(database_url, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800)
        return _engine





