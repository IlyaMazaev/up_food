import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class NutritionProgram(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'nutrition_programs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    meals_data_json = sqlalchemy.Column(sqlalchemy.JSON, nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo_address = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=f'static/img/file_nutrition_program_preview_error.jpg')

    # some additional fields, currently not used
    date_time_added = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    creator_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    some_additional_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_photo_address(self, address=''):
        """sets photo address
        if it's given, sets it
        if not by default sets name 'file_nutrition_program_preview_id.jpg' in static/img/ folder """
        if address:
            self.photo_address = address
        else:
            self.photo_address = f'static/img/file_nutrition_program_preview_{str(self.id)}.jpg'

    def __repr__(self):
        return f'NutritionProgram({str(self.name)})'