from sqlalchemy import Integer, Date, DateTime
from nanohttp import json, settings

from restfulpy.controllers import ModelRestController
from restfulpy.orm import DeclarativeBase, Field, commit, DBSession
from restfulpy.testing import WebAppTestCase
from restfulpy.tests.helpers import MockupApplication


class Event(DeclarativeBase):
    __tablename__ = 'event'
    id = Field(Integer, primary_key=True)
    date = Field(Date, nullable=True)
    datetime = Field(DateTime, nullable=True)


class Root(ModelRestController):
    __model__ = Event

    @json
    @commit
    def post(self):
        e = Event()
        e.update_from_request()
        DBSession.add(e)
        return e


class BaseModelIsoFormatTestCase(WebAppTestCase):
    application = MockupApplication('MockupApplication', Root())
    __configuration__ = '''
    db:
      url: sqlite://    # In memory DB
      echo: false
    '''

    @classmethod
    def configure_app(cls):
        cls.application.configure(force=True)
        settings.merge(cls.__configuration__)
        settings.merge('''
        logging:
          loggers:
            default:
              level: debug
        ''')

    def test_date_format(self):
        # FIXME: has conflict with YYYYMMDD format
        # posix timestamp
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(date='1513434403'), doc=False)
        self.assertEqual(resp['date'], '2017-12-16')

        # YYYY-MM-DD
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(date='2001-01-01'), doc=False)
        self.assertEqual(resp['date'], '2001-01-01')

        # YYYYMMDD
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(date='20010101'), doc=False)
        self.assertEqual(resp['date'], '2001-01-01')

        # YYYY-MM (defaults to 1 for the day)
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(date='2001-01'), doc=False)
        self.assertEqual(resp['date'], '2001-01-01')

        # YYYY (defaults to 1 for month and day)
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(date='2001'), doc=False)
        self.assertEqual(resp['date'], '2001-01-01')

        # None iso date format (YYYY-MM-D is not valid date format)
        self.request('ALL', 'POST', '/', params=dict(date='2001-01-1'), doc=False, expected_status=400)

        # None iso date format (YYYYMM is not valid date format)
        self.request('ALL', 'POST', '/', params=dict(date='200101'), doc=False, expected_status=400)

        # None iso date format (year has 2 digits)
        self.request('ALL', 'POST', '/', params=dict(date='01-01-01'), doc=False, expected_status=400)

        # None iso date format (dash char should be delimiter)
        self.request('ALL', 'POST', '/', params=dict(date='2001/01/01'), doc=False, expected_status=400)

    def test_datetime_format(self):
        # datetime allows contain microseconds
        self.request('ALL', 'POST', '/', params=dict(datetime='2017-10-10T10:10:00.12313'), doc=False)

        self.request(
            'ALL', 'POST', '/', params=dict(datetime='2017-10-10T10:10:00.'), doc=False, expected_status=400
        )

        self.request('ALL', 'POST', '/', params=dict(datetime='2017-10-10T10:10:00'), doc=False)

        # Invalid month value
        self.request(
            'ALL', 'POST', '/', params=dict(datetime='2017-13-10T10:10:00'), doc=False, expected_status=400
        )

        # Invalid datetime format
        self.request(
            'ALL', 'POST', '/', params=dict(datetime='InvalidDatetime'), doc=False, expected_status=400
        )

        # datetime might not have ending Z
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(datetime='2017-10-10T10:10:00.4546'), doc=False)
        self.assertEqual(resp['datetime'], '2017-10-10T10:10:00.004546Z')

        # datetime containing ending Z
        resp, ___ = self.request('ALL', 'POST', '/', params=dict(datetime='2017-10-10T10:10:00.4546Z'), doc=False)
        self.assertEqual(resp['datetime'], '2017-10-10T10:10:00.004546Z')

