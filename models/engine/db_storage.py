#!/user/bin/python3
"""
Database storage engine
"""
from os import getenv
from sqlalchemy import create_engine


class DBStorage():
    __engine = None
    __session = None

    def __init__(self):

        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        database = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+msqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database)
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session)
        all objects depending of the class name
        """

        mydict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                mydict[key] = elem
        else:
            mylist = [State, City, User, Place, Review, Amenity]
            for elem in mylist:
                query = self.__session.query(elem)
                for elem1 in query:
                    key = "{}.{}".format(type(elem1).__name__, elem1.id)
                    mydict[key] = elem1
        return (mydict)

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)

    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()
