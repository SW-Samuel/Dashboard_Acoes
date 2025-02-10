from sqlalchemy import create_engine, Integer, String, Boolean, Column
from sqlalchemy.orm import sessionmaker, declarative_base

db = create_engine('sqlite:///database/swco.db')
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    password = Column('password', String)
    email = Column('email', String)
    admin = Column('admin', Boolean)

    def __init__(self, name, password, email, admin):
        self.name = name
        self.password = password
        self.email = email
        self.admin = admin

Base.metadata.create_all(bind=db)