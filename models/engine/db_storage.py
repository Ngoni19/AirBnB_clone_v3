#!/usr/bin/python3
'''
    Define class DatabaseStorage
'''
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    '''
        Create the SQLalchemy database
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            Create--> Engine && link to MySQL databse
        '''
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
             Database session --> Query
        '''
        data_dic = {}

        if cls != "":
            obj01 = self.__session.query(models.classes[cls]).all()
            for obj in obj01:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                data_dic[key] = obj
            return data_dic
        else:
            for x, v in models.classes.items():
                if x != "BaseModel":
                    obj01 = self.__session.query(v).all()
                    if len(obj01) > 0:
                        for obj in obj01:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            data_dic[key] = obj
            return data_dic

    def new(self, obj):
        '''
            Add object to current database session
        '''
        self.__session.add(obj)

    def save(self):
        '''
            current database session-->Commit changes
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            Delete from current db session
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
            current database session --> Commit changes
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        '''
            Get rid of private session attri
        '''
        self.__session.close()

    def get(self, cls, id):
        '''
             name & id --> Retrieve obj w/class
        '''
        result = None
        try:
            obj01 = self.__session.query(models.classes[cls]).all()
            for obj in obj01:
                if obj.id == id:
                    result = obj
        except BaseException:
            pass
        return result

    def count(self, cls=None):
        '''
            Count num objects in DBstorage
        '''
        cls_counter = 0

        if cls is not None:
            obj01 = self.__session.query(models.classes[cls]).all()
            cls_counter = len(obj01)
        else:
            for x, v in models.classes.items():
                if x != "BaseModel":
                    obj01 = self.__session.query(models.classes[x]).all()
                    cls_counter += len(obj01)
        return cls_counter
