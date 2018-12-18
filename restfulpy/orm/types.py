import ujson
from sqlalchemy import Unicode, TypeDecorator


class FakeJson(TypeDecorator):  # pragma: no cover
    impl = Unicode(3000)

    def process_bind_param(self, value, engine):
        return ujson.dumps(value)

    def process_result_value(self, value, engine):
        if value is None:
            return None

        return ujson.loads(value)
