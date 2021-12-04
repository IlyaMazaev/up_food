import datetime

import sqlalchemy

from data.db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    tags = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo_address = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=f'static/img/file_error.jpg')
    store = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # some additional fields, currently not used
    date_time_added = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    creator_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    some_additional_info = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_photo_address(self, address=''):
        """sets photo address
        if it's given, sets it
        if not by default sets name 'file_recipe name.jpg' in static/img/ folder """
        if address:
            self.photo_address = address
        else:
            self.photo_address = f'static/img/file_{str(self.name)}.jpg'

    def __repr__(self):
        return f'Product({str(self.name)}, {str(self.store)}, {self.price})'

    def get_json_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'type': self.type,
            'tags': self.tags,
            'photo_address': self.photo_address,
            'store': self.store,
            'date_time_added': self.date_time_added,
            'creator_info': self.creator_info,
            'some_additional_info': self.some_additional_info
        }
