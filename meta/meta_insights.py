from datetime import datetime, timedelta
from pymongo.errors import BulkWriteError
from db import db
import json

from meta.utils import *


class MetaInsights:
    def __init__(self,account,level="ad",fields=None):
        self.account = account
        self.level = level
        self.fields = fields

    def insert_levels(self,collection):
        try:
            params = {
                "level":self.level
            }
            level = self.account.get_insights(params=params,fields=self.fields)
            level = [dict(item) for item in level]

            for item in level:
                item.pop("date_start")
                item.pop("date_stop")

            result = db[collection].insert_many(level)

            result = {
                "acknowledged": result.acknowledged,
                "inserted_ids":result.inserted_ids
            }

            return json.dumps(result,default=str)

        except BulkWriteError as err:
            result = err.details["writeErrors"][0]
            result = {
                "message": f"Bulk write error: {err}",
                }

            return result

    def insert_ad_timeseries(self,days:int):
        today = datetime.today().date()
        inserted_ids = []

        for i in range(1, days):
            decrease = timedelta(days=i)
            _date = str(today - decrease)

            params = {'time_range': {'since': _date, 'until': _date}, 'level': self.level}

            ad_level = self.account.get_insights(params=params, fields=self.fields)
            ad_level = [dict(item) for item in ad_level]

            result = db["ads"].insert_many(ad_level)

            result = {
                "acknowledged": result.acknowledged,
                "inserted_ids":result.inserted_ids
                }

            print(json.dumps(result, default=str))

        return result










