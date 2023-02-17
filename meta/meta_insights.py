from datetime import datetime, timedelta
from pprint import pprint
from db import db
import json

from mysql_orm.models import AdSeries,Ads,AgeGender,Country
from mysql_orm import session


class MetaInsights:
    def __init__(self,account,level="ad",fields=None):
        self.account = account
        self.level = level
        self.fields = fields

    def insert_daily_ad_series(self):
        params = {
            "level":self.level,
            "date_preset":"yesterday"
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
                                 video_view = actions.get("video_view",0),
                                 comment = actions.get("comment",0),
                                 link_click = actions.get("link_click",0),
                                 post_reaction = actions.get("post_reaction",0),
                                 landing_page_view = actions.get("landing_page_view",0),
                                 post_engagement = actions.get("post_engagement",0),
                                 leadgen_grouped = actions.get("leadgen_grouped",0),
                                 lead = actions.get("lead",0),
                                 page_engagement = actions.get("page_engagement",0),
                                 onsite_conversion_post_save = actions.get("onsite_conversion_post_save",0),
                                 onsite_conversion_lead_grouped = actions.get("onsite_conversion_lead_grouped",0),
                                 offsite_conversion_fb_pixel_lead = actions.get("offsite_conversion_fb_pixel_lead",0),
                                 frequency = ad["frequency"]
                                 )

            session.add(ad_series)
            session.commit()

    def insert_daily_age_gender(self):
        params = {
            "level": self.level,
            "date_preset":"yesterday",
            "breakdowns":["age","gender"]
        }

        age_gender_today = self.account.get_insights(params=params,fields=self.fields)
        age_gender_today = [dict(item) for item in age_gender_today]

        actions = {}
        for ad in age_gender_today:
            if ad.get("actions",None):
                for _type in ad["actions"]:
                    actions[_type["action_type"]] = _type["value"]


            age_gender = AgeGender(
                ad_id=ad["ad_id"],
                age = ad["age"],
                gender = ad["gender"],
                date = ad["date_start"],
                impressions = ad["impressions"],
                clicks = ad["clicks"],
                total_spend = ad["spend"],
                video_view=actions.get("video_view", 0),
                comment=actions.get("comment", 0),
                link_click=actions.get("link_click", 0),
                post_reaction=actions.get("post_reaction", 0),
                landing_page_view=actions.get("landing_page_view", 0),
                post_engagement=actions.get("post_engagement", 0),
                leadgen_grouped=actions.get("leadgen_grouped", 0),
                lead=actions.get("lead", 0),
                page_engagement=actions.get("page_engagement", 0),
                onsite_conversion_post_save=actions.get("onsite_conversion_post_save", 0),
                onsite_conversion_lead_grouped=actions.get("onsite_conversion_lead_grouped", 0),
                offsite_conversion_fb_pixel_lead=actions.get("offsite_conversion_fb_pixel_lead", 0),
                frequency = ad["frequency"]
            )

            session.add(age_gender)
            session.commit()


    def insert_daily_country(self):
        params = {
            "level": self.level,
            "date_preset":"yesterday",
            "breakdowns":["country"]
        }

        country_today = self.account.get_insights(params=params,fields=self.fields)
        country_today = [dict(item) for item in country_today]

        actions = {}
        for ad in country_today:
            if ad.get("actions",None):
                for _type in ad["actions"]:
                    actions[_type["action_type"]] = _type["value"]

            country = Country(
                ad_id=ad["ad_id"],
                country = ad["country"],
                date = ad["date_start"],
                impressions = ad["impressions"],
                clicks = ad["clicks"],
                total_spend = ad["spend"],
                video_view=actions.get("video_view", 0),
                comment=actions.get("comment", 0),
                link_click=actions.get("link_click", 0),
                post_reaction=actions.get("post_reaction", 0),
                landing_page_view=actions.get("landing_page_view", 0),
                post_engagement=actions.get("post_engagement", 0),
                leadgen_grouped=actions.get("leadgen_grouped", 0),
                lead=actions.get("lead", 0),
                page_engagement=actions.get("page_engagement", 0),
                onsite_conversion_post_save=actions.get("onsite_conversion_post_save", 0),
                onsite_conversion_lead_grouped=actions.get("onsite_conversion_lead_grouped", 0),
                offsite_conversion_fb_pixel_lead=actions.get("offsite_conversion_fb_pixel_lead", 0),
                frequency = ad["frequency"]
            )

            session.add(country)
            session.commit()




























































