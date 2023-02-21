from datetime import datetime, timedelta,date
from pprint import pprint
from calendar import monthrange
import logging
import json
from pathlib import Path

from mysql_orm.models import AdSeries,Ads,AgeGender,Country
from mysql_orm import session
from sqlalchemy import update

import os
basedir = str(Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute())

class MetaInsights:
    def __init__(self,account,level="ad",fields=None):
        self.account = account
        self.level = level
        self.fields = fields
        self.today = date.today()
        self.dtime = str(datetime.now())
        self.insertion_logs = basedir+"/logs/insertion_errors.logs"
        self.update_logs = basedir+"/logs/update_errors.logs"
    def insert_daily_ad_series(self):
        params = {
            "level":self.level,
            "date_preset":"yesterday"
        }

        logging.basicConfig(filename=self.insertion_logs, level=logging.ERROR)

        ad_insights_today = self.account.get_insights(params=params,fields=self.fields)
        ad_insights_today = [dict(item) for item in ad_insights_today]
        actions = {}

        for ad in ad_insights_today:
            if ad.get("actions",None):
                for _type in ad["actions"]:
                    actions[_type["action_type"]] = _type["value"]

            try:
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
                print("Ad series inserted succesfully")

            except Exception as e:
                logging.error(f"{self.dtime} Exception occurred while inserting ad series: {e}")
                session.rollback()

    def insert_daily_age_gender(self):
        params = {
            "level": self.level,
            "date_preset":"yesterday",
            "breakdowns":["age","gender"]
        }

        logging.basicConfig(filename=self.insertion_logs, level=logging.ERROR)

        age_gender_today = self.account.get_insights(params=params,fields=self.fields)
        age_gender_today = [dict(item) for item in age_gender_today]

        actions = {}
        for ad in age_gender_today:
            if ad.get("actions",None):
                for _type in ad["actions"]:
                    actions[_type["action_type"]] = _type["value"]

            try:
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
                print("Age gender inserted succesfully")

            except Exception as e:
                logging.error(f"{self.dtime} Exception occurred while inserting ad series: {e}")
                session.rollback()

    def insert_daily_country(self):
        params = {
            "level": self.level,
            "date_preset":"yesterday",
            "breakdowns":["country"]
        }

        logging.basicConfig(filename=self.insertion_logs, level=logging.ERROR)

        country_today = self.account.get_insights(params=params,fields=self.fields)
        country_today = [dict(item) for item in country_today]

        actions = {}
        for ad in country_today:
            if ad.get("actions",None):
                for _type in ad["actions"]:
                    actions[_type["action_type"]] = _type["value"]

            try:
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
                print("Countries inserted succesfully")

            except Exception as e:
                logging.error(f"{self.dtime} Exception occurred while inserting ad series: {e}")
                session.rollback()

    def update_weekly_ad_series(self):

        logging.basicConfig(filename=self.update_logs, level=logging.ERROR)

        for i in range(1, 8):
            day_decrease = timedelta(days=i)
            date_to_use = self.today - timedelta(days=1)
            date_to_use = date_to_use - day_decrease
            strdate = str(date_to_use.year) + '-' + str(date_to_use.month) + '-' + str(date_to_use.day)

            params = {
                "level": self.level,
                'time_range': {'since': strdate, 'until': strdate},
            }

            weekly_ad_series = self.account.get_insights(params=params, fields=self.fields)
            weekly_ad_series = [dict(item) for item in weekly_ad_series]
            actions = {}
            for ad in weekly_ad_series:
                if ad.get("actions", None):
                    for _type in ad["actions"]:
                        actions[_type["action_type"]] = _type["value"]

                try:
                    session.query(AdSeries).filter(AdSeries.ad_id == ad["ad_id"],
                                                    AdSeries.date == ad["date_start"]) \
                        .update({"impressions": ad["impressions"],
                                 "clicks": ad["clicks"],
                                 "total_spend": ad["spend"],
                                 "video_view": actions.get("video_view", 0),
                                 "comment": actions.get("comment", 0),
                                 "link_click": actions.get("link_click", 0),
                                 "post_reaction": actions.get("post_reaction", 0),
                                 "landing_page_view": actions.get("landing_page_view", 0),
                                 "post_engagement": actions.get("post_engagement", 0),
                                 "leadgen_grouped": actions.get("leadgen_grouped", 0),
                                 "lead": actions.get("lead", 0),
                                 "page_engagement": actions.get("page_engagement", 0),
                                 "onsite_conversion_post_save": actions.get("onsite_conversion_post_save", 0),
                                 "onsite_conversion_lead_grouped": actions.get("onsite_conversion_lead_grouped", 0),
                                 "offsite_conversion_fb_pixel_lead": actions.get("offsite_conversion_fb_pixel_lead", 0),
                                 "frequency": ad["frequency"]})


                    session.commit()
                    print("Weekly ad series updated")

                except Exception as e:
                    error = f"{self.dtime} Exception occurred while updating weekly ad series: {e}"
                    logging.error(error)
                    session.rollback()


    def update_weekly_age_gender(self):

        logging.basicConfig(filename=self.update_logs, level=logging.ERROR)

        for i in range(1, 8):
            day_decrease = timedelta(days=i)
            date_to_use = self.today - timedelta(days=1)
            date_to_use = date_to_use - day_decrease
            strdate = str(date_to_use.year) + '-' + str(date_to_use.month) + '-' + str(date_to_use.day)

            params = {
                "level": self.level,
                'time_range': {'since': strdate, 'until': strdate},
                "breakdowns": ["age","gender"]
            }

            age_gender_weekly = self.account.get_insights(params=params, fields=self.fields)
            age_gender_weekly = [dict(item) for item in age_gender_weekly]
            actions = {}
            for ad in age_gender_weekly:
                if ad.get("actions", None):
                    for _type in ad["actions"]:
                        actions[_type["action_type"]] = _type["value"]

                try:
                    session.query(AgeGender).filter(AgeGender.ad_id == ad["ad_id"],
                                                      AgeGender.age == ad["age"],
                                                      AgeGender.gender == ad["gender"],
                                                      AgeGender.date == ad["date_start"]) \
                                                      .update({"impressions": ad["impressions"],
                                                                 "clicks": ad["clicks"],
                                                                 "total_spend": ad["spend"],
                                                                 "video_view": actions.get("video_view", 0),
                                                                 "comment": actions.get("comment", 0),
                                                                 "link_click": actions.get("link_click", 0),
                                                                 "post_reaction": actions.get("post_reaction", 0),
                                                                 "landing_page_view": actions.get("landing_page_view", 0),
                                                                 "post_engagement": actions.get("post_engagement", 0),
                                                                 "leadgen_grouped": actions.get("leadgen_grouped", 0),
                                                                 "lead": actions.get("lead", 0),
                                                                 "page_engagement": actions.get("page_engagement", 0),
                                                                 "onsite_conversion_post_save": actions.get("onsite_conversion_post_save", 0),
                                                                 "onsite_conversion_lead_grouped": actions.get("onsite_conversion_lead_grouped", 0),
                                                                 "offsite_conversion_fb_pixel_lead": actions.get("offsite_conversion_fb_pixel_lead", 0),

                                                                "frequency": ad["frequency"]})

                    session.commit()
                    print("Weekly age gender updated")

                except Exception as e:
                    error = f"{self.dtime} Exception occurred while updating weekly age_gender: {e}"
                    logging.error(error)
                    session.rollback()


    def update_weekly_country(self):

        logging.basicConfig(filename=self.update_logs, level=logging.ERROR)

        for i in range(1, 8):
            day_decrease = timedelta(days=i)
            date_to_use = self.today - timedelta(days=1)
            date_to_use = date_to_use - day_decrease
            strdate = str(date_to_use.year) + '-' + str(date_to_use.month) + '-' + str(date_to_use.day)

            params = {
                "level": self.level,
                'time_range': {'since': strdate, 'until': strdate},
                "breakdowns": ["country"]
            }

            country_weekly = self.account.get_insights(params=params, fields=self.fields)
            country_weekly = [dict(item) for item in country_weekly]
            actions = {}
            for ad in country_weekly:
                if ad.get("actions", None):
                    for _type in ad["actions"]:
                        actions[_type["action_type"]] = _type["value"]


                try:
                    session.query(Country).filter(Country.ad_id == ad["ad_id"],
                                            Country.country == ad["country"],
                                            Country.date == ad["date_start"])\
                                             .update({"impressions":ad["impressions"],
                                                       "clicks":ad["clicks"],
                                                       "total_spend":ad["spend"],
                                                       "video_view":actions.get("video_view", 0),
                                                       "comment":actions.get("comment", 0),
                                                       "link_click":actions.get("link_click", 0),
                                                       "post_reaction":actions.get("post_reaction", 0),
                                                       "landing_page_view":actions.get("landing_page_view", 0),
                                                       "post_engagement":actions.get("post_engagement", 0),
                                                       "leadgen_grouped":actions.get("leadgen_grouped", 0),
                                                       "lead":actions.get("lead", 0),
                                                       "page_engagement":actions.get("page_engagement", 0),
                                                       "onsite_conversion_post_save":actions.get("onsite_conversion_post_save", 0),
                                                       "onsite_conversion_lead_grouped":actions.get("onsite_conversion_lead_grouped", 0),
                                                       "offsite_conversion_fb_pixel_lead":actions.get("offsite_conversion_fb_pixel_lead", 0),
                                                       "frequency":ad["frequency"]})


                    session.commit()
                    print("Weekly countries updated")

                except Exception as e:
                    error = f"{self.dtime} Exception occurred while updating weekly country: {e}"
                    logging.error(error)
                    session.rollback()


    def update_monthly_ad_series(self):
        dt = self.today - timedelta(days=3)
        year_and_month = monthrange(dt.year,dt.month)
        month_to_use = year_and_month[1]
        logging.basicConfig(filename=self.update_logs, level=logging.ERROR)

        for i in range(1, month_to_use):
            day_decrease = timedelta(days=i)
            date_to_use = self.today - timedelta(days=3)
            date_to_use = date_to_use - day_decrease
            strdate = str(date_to_use.year) + '-' + str(date_to_use.month) + '-' + str(date_to_use.day)

            params = {
                "level": self.level,
                'time_range': {'since': strdate, 'until': strdate},
            }

            monthly_ad_series = self.account.get_insights(params=params, fields=self.fields)
            monthly_ad_series = [dict(item) for item in monthly_ad_series]
            actions = {}
            for ad in monthly_ad_series:
                if ad.get("actions", None):
                    for _type in ad["actions"]:
                        actions[_type["action_type"]] = _type["value"]

                try:
                    session.query(AdSeries).filter(AdSeries.ad_id == ad["ad_id"],
                                                    AdSeries.date == ad["date_start"]) \
                        .update({"impressions": ad["impressions"],
                                 "clicks": ad["clicks"],
                                 "total_spend": ad["spend"],
                                 "video_view": actions.get("video_view", 0),
                                 "comment": actions.get("comment", 0),
                                 "link_click": actions.get("link_click", 0),
                                 "post_reaction": actions.get("post_reaction", 0),
                                 "landing_page_view": actions.get("landing_page_view", 0),
                                 "post_engagement": actions.get("post_engagement", 0),
                                 "leadgen_grouped": actions.get("leadgen_grouped", 0),
                                 "lead": actions.get("lead", 0),
                                 "page_engagement": actions.get("page_engagement", 0),
                                 "onsite_conversion_post_save": actions.get("onsite_conversion_post_save", 0),
                                 "onsite_conversion_lead_grouped": actions.get("onsite_conversion_lead_grouped", 0),
                                 "offsite_conversion_fb_pixel_lead": actions.get("offsite_conversion_fb_pixel_lead", 0),
                                 "frequency": ad["frequency"]})


                    session.commit()
                    print("Monthly ad series updated")

                except Exception as e:
                    error = f"{self.dtime} Exception occurred while updating monthly ad_series: {e}"
                    logging.error(error)
                    session.rollback()


    def update_monthly_age_and_gender(self):
        dt = self.today - timedelta(days=3)
        year_and_month = monthrange(dt.year, dt.month)
        month_to_use = year_and_month[1]
        logging.basicConfig(filename=self.update_logs, level=logging.ERROR)

        for i in range(1, month_to_use):
            day_decrease = timedelta(days=i)
            date_to_use = self.today - timedelta(days=3)
            date_to_use = date_to_use - day_decrease
            strdate = str(date_to_use.year) + '-' + str(date_to_use.month) + '-' + str(date_to_use.day)

            params = {
                "level": self.level,
                'time_range': {'since': strdate, 'until': strdate},
                "breakdowns": ["age", "gender"]
            }

            monthly_age_and_gender = self.account.get_insights(params=params, fields=self.fields)
            monthly_age_and_gender = [dict(item) for item in monthly_age_and_gender]
            actions = {}
            for ad in monthly_age_and_gender:
                if ad.get("actions", None):
                    for _type in ad["actions"]:
                        actions[_type["action_type"]] = _type["value"]

                try:
                    session.query(AgeGender).filter(AgeGender.ad_id == ad["ad_id"],
                                                    AgeGender.age == ad["age"],
                                                    AgeGender.gender == ad["gender"],
                                                    AgeGender.date == ad["date_start"]) \
                        .update({"impressions": ad["impressions"],
                                 "clicks": ad["clicks"],
                                 "total_spend": ad["spend"],
                                 "video_view": actions.get("video_view", 0),
                                 "comment": actions.get("comment", 0),
                                 "link_click": actions.get("link_click", 0),
                                 "post_reaction": actions.get("post_reaction", 0),
                                 "landing_page_view": actions.get("landing_page_view", 0),
                                 "post_engagement": actions.get("post_engagement", 0),
                                 "leadgen_grouped": actions.get("leadgen_grouped", 0),
                                 "lead": actions.get("lead", 0),
                                 "page_engagement": actions.get("page_engagement", 0),
                                 "onsite_conversion_post_save": actions.get("onsite_conversion_post_save", 0),
                                 "onsite_conversion_lead_grouped": actions.get("onsite_conversion_lead_grouped", 0),
                                 "offsite_conversion_fb_pixel_lead": actions.get("offsite_conversion_fb_pixel_lead", 0),
                                 "frequency": ad["frequency"]})

                    session.commit()
                    print("Monthly age gender updated")


                except Exception as e:
                    error = f"{self.dtime} Exception occurred while updating monthly age_gender: {e}"
                    logging.error(error)
                    session.rollback()



    def update_monthly_country(self):
        dt = self.today - timedelta(days=3)
        year_and_month = monthrange(dt.year, dt.month)
        month_to_use = year_and_month[1]
        logging.basicConfig(filename=self.update_logs, level=logging.ERROR)

        for i in range(1, month_to_use):
            day_decrease = timedelta(days=i)
            date_to_use = self.today  - timedelta(days=3)
            date_to_use = date_to_use - day_decrease
            strdate = str(date_to_use.year) + '-' + str(date_to_use.month) + '-' + str(date_to_use.day)

            params = {
                "level": self.level,
                'time_range': {'since': strdate, 'until': strdate},
                "breakdowns": ["country"]
            }

            monthly_country = self.account.get_insights(params=params, fields=self.fields)
            monthly_country = [dict(item) for item in monthly_country]
            actions = {}
            for ad in monthly_country:
                if ad.get("actions", None):
                    for _type in ad["actions"]:
                        actions[_type["action_type"]] = _type["value"]

                try:
                    session.query(Country).filter(Country.ad_id == ad["ad_id"],
                                                  Country.country == ad["country"],
                                                  Country.date == ad["date_start"]) \
                        .update({"impressions": ad["impressions"],
                                 "clicks": ad["clicks"],
                                 "total_spend": ad["spend"],
                                 "video_view": actions.get("video_view", 0),
                                 "comment": actions.get("comment", 0),
                                 "link_click": actions.get("link_click", 0),
                                 "post_reaction": actions.get("post_reaction", 0),
                                 "landing_page_view": actions.get("landing_page_view", 0),
                                 "post_engagement": actions.get("post_engagement", 0),
                                 "leadgen_grouped": actions.get("leadgen_grouped", 0),
                                 "lead": actions.get("lead", 0),
                                 "page_engagement": actions.get("page_engagement", 0),
                                 "onsite_conversion_post_save": actions.get("onsite_conversion_post_save", 0),
                                 "onsite_conversion_lead_grouped": actions.get("onsite_conversion_lead_grouped", 0),
                                 "offsite_conversion_fb_pixel_lead": actions.get("offsite_conversion_fb_pixel_lead", 0),
                                 "frequency": ad["frequency"]})

                    session.commit()
                    print("Monthly countries updated")

                except Exception as e:
                    error = f"{self.dtime} Exception occurred while updating monthly country: {e}"
                    logging.error(error)
                    session.rollback()