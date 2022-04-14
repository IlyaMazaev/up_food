import sqlalchemy

from data.db_session import SqlAlchemyBase


class Picture(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    call_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo_address = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='static/img/file_error.jpg')

    def __repr__(self):
        return f'Image(id:{str(self.id)})'

