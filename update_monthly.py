from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from dotenv import load_dotenv
import json
import os

from meta.meta_insights import MetaInsights

if __name__ == "__main__":

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

    for acc in account:
        my_account = AdAccount(acc)

        meta_insights = MetaInsights(
            account=my_account,
            fields=ad_fields,
            level="ad"
            )

        print("Ad series update...")
        meta_insights.update_monthly_ad_series()
        meta_insights.update_weekly_age_gender()
        meta_insights.update_monthly_country()

