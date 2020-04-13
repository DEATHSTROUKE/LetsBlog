from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    surname = sa.Column(sa.String)
    name = sa.Column(sa.String)
    nick = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)
    modified_date = sa.Column(sa.DateTime, default=datetime.now)
    info = sa.Column(sa.String)
    avatar = sa.Column(sa.String)
    rate = sa.Column(sa.Integer)
    date_born = sa.Column(sa.DateTime)
    date_register = sa.Column(sa.DateTime, default=datetime.now)
    work = sa.Column(sa.String)
    is_author = sa.Column(sa.Boolean, default=False)
    article = orm.relation('Article', back_populates='user')
    comment = orm.relation('Comment', back_populates='user')
    sub_person = orm.relation('SubPerson', back_populates='user1')
    sub_category = orm.relation('SubCategory', back_populates='user1')
    user_bookmarks = orm.relation('UserBookmark', back_populates='user1')

    def __repr__(self):
        return f'<User> {self.name} {self.surname}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
