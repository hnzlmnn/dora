import binascii

from peewee import CharField


class BytesField(CharField):
    field_type = 'char'

    def __init__(self, max_length, *args, **kwargs):
        super().__init__(*args, max_length=max_length * 2, **kwargs)

    def db_value(self, value):
        return binascii.b2a_hex(value)

    def python_value(self, value):
        return binascii.a2b_hex(value)
