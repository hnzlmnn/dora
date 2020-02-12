import base64
import binascii
from typing import Union

from peewee import DatabaseProxy, Model, CharField, BooleanField, DateTimeField, IntegerField, ForeignKeyField, \
    CompositeKey

from db.fields import BytesField

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Entry(BaseModel):
    id = IntegerField(primary_key=True)
    context = CharField(32)
    source = CharField(40)
    v6 = BooleanField()
    received_at = DateTimeField()
    line = IntegerField()
    data = BytesField(64)

    def summary(self):
        return f"{self.received_at}: received line {self.line} from {str(self.source)} with content '{self.binary()}' for '{self.context}'"

    def _decoded(self, encoding=None) -> Union[str, None]:
        try:
            data = base64.b64decode(self.data, validate=True)
            if encoding:
                return data.decode(encoding)
            return data
        except (binascii.Error, UnicodeDecodeError):
            return None

    def ascii(self) -> Union[str, None]:
        return self._decoded('ascii')

    def binary(self) -> Union[str, None]:
        return self._decoded()

    def to_json(self):
        return dict(
            id=self.id,
            source=self.source,
            v6=self.v6,
            received_at=self.received_at.timestamp(),
            context=self.context,
            line=self.line,
            data=self.data.decode("ascii"),
        )


class Line(BaseModel):
    context = CharField(32)
    line = IntegerField()
    entry = ForeignKeyField(Entry)
    selected_at = DateTimeField()

    class Meta:
        primary_key = CompositeKey('context', 'line')

    def summary(self):
        return f"{self.selected_at}: {self.context}:{self.line} -> {self.entry}"

    def to_json(self):
        return dict(
            context=self.context,
            line=self.line,
            entry=self.entry,
            selected_at=self.selected_at.timestamp(),
        )
