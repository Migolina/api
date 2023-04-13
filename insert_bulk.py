from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from dotenv import load_dotenv
from datetime import datetime, timedelta,date
from calendar import monthrange
from pprint import pprint
import json
import os

from meta.meta_insights import MetaInsights
from mysql_orm import session
from mysql_orm.models import AdSeries

load_dotenv()
app_id = str(os.getenv("APP_ID"))
app_secret = str(os.getenv("APP_SECRET"))
access_token = str(os.getenv("ACCESS_TOKEN"))
account = json.loads(os.getenv("ACCOUNT"))

FacebookAdsApi.init(app_id, app_secret, access_token)

ad_fields = [
    AdsInsights.Field.ad_id,
    AdsInsights.Field.date_start,
    AdsInsights.Field.impressions,
    AdsInsights.Field.clicks,
    AdsInsights.Field.spend,
    AdsInsights.Field.actions,
    AdsInsights.Field.frequency
]

my_account = AdAccount(account[0])

since = "2023-01-01"
until = "2023-04-05"

for i in range(1,60):
    dt = (date.today() - timedelta(i)).strftime("%Y-%m-%d")
    params = {
        'level': 'ad',
        'time_range': {
            'since': dt,
            'until': dt
        }
    }
    insights = my_account.get_insights(params=params,fields=ad_fields)
    insights = [dict(item) for item in insights]
    actions = {}
    for ad in insights:
        if ad.get('actions'):
            for _type in ad['actions']:
                actions[_type['action_type']] = _type['value']

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
            print(f'ad series {dt} inserted')
        except Exception as e:
            print(f"Exception occurred while inserting ad series: {e}")
            session.rollback()
