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

    Id = Column(Integer, primary_key=True)
    userName = Column(String(20), nullable=False)
    firstName = Column(String(20), nullable=False)
    lastName = Column(String(25), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(String(10))
    userStatus = Column(Integer, nullable=False)

    def __repr__(self):
        return "<User('%s','%s','%s','%s','%s','%s','%s','%s',)>" % (self.Id, self.userStatus, self.userName,
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
    id = Column(Integer, primary_key=True)
    shipDate = Column(DateTime, nullable=False)
    packed = Column(Boolean, default=False)
    statusCustomid = Column(Integer, ForeignKey('statusCustom.statusCustom'))
    userid = Column(Integer, ForeignKey('user.Id'))
    productionid=Column(Integer, ForeignKey('production.id'))

    statusCustom = orm.relationship("StatusCustom")
    userCustom = orm.relationship("User")
    productionCustom = orm.relationship("Production")
    def __repr__(self):
        return "<Custom('%s','%s','%s')>" % (self.id, self.shipDate, self.packed)

    def __str__(self):
        return f"id: {self.id}\n"\
               f"shipDate: {self.shipDate}\n"\
               f"packed: {self.packed}\n"


class Production(Base):
    __tablename__ = "production"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    number = Column(Integer, nullable=False)
    statusProductid = Column(Integer, ForeignKey('statusProduct.statusProduct'))


    statusProduct = orm.relationship("StatusProduction")

    def __repr__(self):
        return "<Production('%s','%s','%s')>" % (self.id, self.name, self.number)

    def __str__(self):
        return f"id: {self.id}\n"\
               f"name: {self.name}\n"\
               f"number: {self.number}\n"



class StatusProduction(Base):
    __tablename__ = "statusProduct"

    statusProduct = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


    def __repr__(self):
        return "<StatusProduction('%s','%s')>" % (self.statusProduct, self.name)

    def __str__(self):
        return f"statusProduct: {self.statusProduct}\n"\
               f"name: {self.name}\n"

class StatusCustom(Base):
    __tablename__ = "statusCustom"

    statusCustom = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


    def __repr__(self):
        return "<StatusCustom('%s','%s')>" % (self.statusCustom, self.name)

    def __str__(self):
        return f"statusCustom: {self.statusCustom}\n"\
               f"name: {self.name}\n"











# class PlaylistsSongs(Base):
#     __tablename__ = "playlistssongs"
#
#     songId = Column(Integer, ForeignKey('song.songId'))
#     playlistId = Column(Integer, ForeignKey('playlist.playlistId'))
#
#     song = orm.relationship("Song")
#     playlist = orm.relationship("Playlist")
#
#     __table_args__ = (
#         PrimaryKeyConstraint('songId', 'playlistId'), {}
#     )

# class PrivatePlaylist(Base):
#     __tablename__ = "privateplaylist"
#
#     privateplaylistId = Column(Integer, primary_key=True)
#     playlistId = Column(Integer, ForeignKey('playlist.playlistId'))
#     Id = Column(Integer, ForeignKey('user.Id'))
#
#     user = orm.relationship("User")
#     playlist = orm.relationship("Playlist")
#
#     def __repr__(self):
#         return "<Privateplaylist('%s')>" % (self.privateplaylistId)
#
#     def __str__(self):
#         return f"privateplaylistId: {self.privateplaylistId}\n"