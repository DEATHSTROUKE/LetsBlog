from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Tag(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tags'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, unique=True)
    tag_article = orm.relation('TagArticle', back_populates='tag1')
