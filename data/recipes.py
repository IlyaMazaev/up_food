import datetime
import sqlalchemy

from data.db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    ingredients = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    how_to_cook = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo_address = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=f'static/img/file_error.jpg')
    # some additional fields, currently not used
    date_time_added = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    creator_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    some_additional_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_photo_address(self, address=''):
        '''sets photo address
        if it's given, sets it
        if not by default sets name 'file_recipe name.jpg' in static/img/ folder '''
        if address:
            self.photo_address = address
        else:
            self.photo_address = f'static/img/file_{str(self.name)}.jpg'

    def __repr__(self):
        return f'Recipe({str(self.name)})'
