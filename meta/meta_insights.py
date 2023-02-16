from datetime import datetime, timedelta
from pymongo.errors import BulkWriteError
from db import db
import json
from pprint import pprint

from mysql_orm.models import AdSeries,Ads
from mysql_orm import session


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

    def insert_daily_ad_series(self):
        params = {
            "level":self.level,
            "date_preset":"today"
        }

        ad_insights_today = self.account.get_insights(params=params,fields=self.fields)
        ad_insights_today = [dict(item) for item in ad_insights_today]
        actions = {}
        for ad in ad_insights_today:
            if ad.get("actions",None):
                for _type in ad["actions"]:
                    actions[_type["action_type"]] = _type["value"]


            ad_series = AdSeries(ad_id = ad["ad_id"],
                                 date = ad["date_start"],
                                 impressions = ad["impressions"],
                                 clicks = ad["clicks"],
                                 total_spend = ad["spend"],
                                 video_view = actions.get("video_view",None),
                                 comment = actions.get("comment",None),
                                 link_click = actions.get("link_click",None),
                                 post_reaction = actions.get("post_reaction",None),
                                 landing_page_view = actions.get("landing_page_view",None),
                                 post_engagement = actions.get("post_engagement",None),
                                 leadgen_grouped = actions.get("leadgen_grouped",None),
                                 lead = actions.get("lead",None),
                                 page_engagement = actions.get("page_engagement",None),
                                 onsite_conversion_post_save = actions.get("onsite_conversion_post_save",None),
                                 onsite_conversion_lead_grouped = actions.get("onsite_conversion_lead_grouped",None),
                                 offsite_conversion_fb_pixel_lead = actions.get("offsite_conversion_fb_pixel_lead",None),
                                 frequency = ad["frequency"]
                                 )

            session.add(ad_series)
            session.commit()




























