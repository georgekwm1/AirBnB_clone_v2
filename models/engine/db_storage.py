#!/usr/bin/python3
""" cantains the DBStorage class"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData
from models.base_model import Base
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from os import environ


class DBStorage:
    """ Defines the DBStorage that responsible for comunicate with MySQL DB"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                environ.get('HBNB_MYSQL_USER'),
                environ.get('HBNB_MYSQL_PWD'),
                environ.get('HBNB_MYSQL_HOST'),
                environ.get('HBNB_MYSQL_DB')
            ),
            pool_pre_ping=True
        )
        if environ.get('HBNB_ENV') == 'test':
            MetaData(self.__engine).reflect().drop_all()
    
    def all(self, cls=None):
        """Query on the current database session"""
        myDict = {}
        if cls:
            print("hello, world\n" * 12)
            for aClass in self.__session.query(eval(cls)).all():
                print("hello, world\n" * 12)
                classKey = f"{aClass.__class__.__name__}.{aClass.id}"
                myDict[classKey] = aClass

        else:
            classTypes = [User, State, City, Amenity, Place, Review]
            for classType in classTypes:
                for aClass in (self.__session.query(eval(classType)).all()):
                    classKey = f"{aClass.__class__.__name__}.{aClass.id}"
                    myDict[classKey] = aClass

        return myDict

    def new(self, obj):
        """adds the object to the current database"""
        self.__session.add(obj)
    
    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
            """create the table in the database and the current session"""
            Base.metadata.create_all(self.__engine)
            Session = scoped_session(sessionmaker(
                self.__engine,
                expire_on_commit=False)
                )
            self.__session = Session()