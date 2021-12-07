import os
import sys

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    BigInteger,
    DateTime,
    Boolean,
    DECIMAL,
    func, PrimaryKeyConstraint,
)
from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session


SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:vika29@localhost:3306/inetshop"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    Id = Column(Integer, primary_key=True, unique=True)
    userName = Column(String(20), nullable=False)
    firstName = Column(String(20), nullable=False)
    lastName = Column(String(25), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False )
    phone = Column(String(10), unique=True)
    userStatus = Column(Integer, nullable=False)

    def __repr__(self):
        return "<User('%sb','%s','%s','%s','%s','%s','%s','%s',)>" % (self.Id, self.userStatus, self.userName,
                                                                     self.firstName, self.lastName, self.email,
                                                                     self.password, self.phone)

    def __str__(self):
        return f"Id: {self.Id}\n" \
               f"userStatus: {self.userStatus}\n" \
               f"userName: {self.userName}\n"\
               f"firstName: {self.firstName}\n" \
               f"lastName: {self.lastName}\n" \
               f"email: {self.email}\n" \
               f"password: {self.password}\n" \
               f"phone: {self.phone}\n"


class Custom(Base):
    __tablename__ = "custom"
    id = Column(Integer, primary_key=True, unique=True)
    shipDate = Column(DateTime, nullable=False)
    statusCustomid = Column(Integer, ForeignKey('statusCustom.statusCustom'))
    userid = Column(Integer, ForeignKey('user.Id'))
    productionid=Column(Integer, ForeignKey('production.id'))

    statusCustom = orm.relationship("StatusCustom")
    userCustom = orm.relationship("User")
    productionCustom = orm.relationship("Production")
    def __repr__(self):
        return "<Custom('%s','%s')>" % (self.id, self.shipDate)

    def __str__(self):
        return f"id: {self.id}\n"\
               f"shipDate: {self.shipDate}\n"


class Production(Base):
    __tablename__ = "production"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(20), nullable=False)
    number = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Production('%s','%s','%s')>" % (self.id, self.name, self.number)

    def __str__(self):
        return f"id: {self.id}\n"\
               f"name: {self.name}\n"\
               f"number: {self.number}\n"


class StatusCustom(Base):
    __tablename__ = "statusCustom"

    statusCustom = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


    def __repr__(self):
        return "<StatusCustom('%s','%s')>" % (self.statusCustom, self.name)

    def __str__(self):
        return f"statusCustom: {self.statusCustom}\n"\
               f"name: {self.name}\n"










