import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    ingredients = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    how_to_cook = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo_address = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='static/img/file_error.jpg')
    link_to_photo_api = sqlalchemy.Column(sqlalchemy.String, nullable=True,
                                          default='https://recipes-db-api.herokuapp.com/api/recipes/photo/error')
    portions = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    types = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    bonded_ingredients = sqlalchemy.Column(sqlalchemy.JSON, nullable=False)
    creator_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # some additional fields, currently not used
    date_time_added = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    some_additional_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_photo_address(self, address=''):
        """sets photo address
        if it's given, sets it
        if not by default sets name 'file_recipe id.jpg' in static/img/ folder """
        if address:
            self.photo_address = address
        else:
            self.photo_address = f'static/img/file_{str(self.id)}.jpg'

        self.link_to_photo_api = f'https://recipes-db-api.herokuapp.com/api/recipes/photo/{str(self.id)}'

    def __repr__(self):
        return f'Recipe({str(self.name)})'

    def get_json_data(self):
        return {'id': self.id,
                'name': self.name,
                'ingredients': self.ingredients,
                'how_to_cook': self.how_to_cook,
                'tags': self.tags,
                'photo_address': self.photo_address,
                'portions': self.portions,
                'time': self.time,
                'types': self.types,
                'date_time_added': self.date_time_added,
                'creator_info': self.creator_info,
                'some_additional_info': self.some_additional_info
                }
