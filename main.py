from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from dotenv import load_dotenv
import os

from facebook.insights import Insights
from meta.meta_insights import MetaInsights


if __name__ == "__main__":

    load_dotenv()

    app_id = str(os.getenv("APP_ID"))
    app_secret = str(os.getenv("APP_SECRET"))
    access_token = str(os.getenv("ACCESS_TOKEN"))
    account = str(os.getenv("ACCOUNT"))

    FacebookAdsApi.init(app_id, app_secret, access_token)
    my_account = AdAccount(account)

    all_fields = [
        AdsInsights.Field.account_id,
        AdsInsights.Field.account_name,
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.adset_id,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.ad_id,
        AdsInsights.Field.ad_name,
        AdsInsights.Field.clicks,
        AdsInsights.Field.conversion_rate_ranking,
        AdsInsights.Field.conversion_values,
        AdsInsights.Field.conversions,
        AdsInsights.Field.converted_product_quantity,
        AdsInsights.Field.converted_product_value,
        AdsInsights.Field.cost_per_conversion,
        AdsInsights.Field.cost_per_estimated_ad_recallers,
        AdsInsights.Field.cost_per_inline_link_click,
        AdsInsights.Field.cost_per_inline_post_engagement,
        AdsInsights.Field.cost_per_unique_click,
        AdsInsights.Field.cost_per_unique_inline_link_click,
        AdsInsights.Field.cpc,
        AdsInsights.Field.cpm,
        AdsInsights.Field.cpp,
        AdsInsights.Field.ctr,
        AdsInsights.Field.dda_results,
        AdsInsights.Field.engagement_rate_ranking,
        AdsInsights.Field.estimated_ad_recall_rate,
        AdsInsights.Field.estimated_ad_recallers,
        AdsInsights.Field.frequency,
        AdsInsights.Field.full_view_impressions,
        AdsInsights.Field.full_view_reach,
        AdsInsights.Field.impressions,
        AdsInsights.Field.inline_link_click_ctr,
        AdsInsights.Field.inline_link_clicks,
        AdsInsights.Field.inline_post_engagement,
        AdsInsights.Field.instant_experience_clicks_to_open,
        AdsInsights.Field.instant_experience_clicks_to_start,
        AdsInsights.Field.instant_experience_outbound_clicks,
        AdsInsights.Field.mobile_app_purchase_roas,
        AdsInsights.Field.objective,
        AdsInsights.Field.optimization_goal,
        AdsInsights.Field.purchase_roas,
        AdsInsights.Field.quality_ranking,
        AdsInsights.Field.reach,
        AdsInsights.Field.social_spend,
        AdsInsights.Field.spend,
        AdsInsights.Field.website_purchase_roas,
        AdsInsights.Field.website_ctr,
        AdsInsights.Field.video_30_sec_watched_actions,
        AdsInsights.Field.outbound_clicks_ctr,
        AdsInsights.Field.outbound_clicks,
        AdsInsights.Field.cost_per_unique_outbound_click,
        AdsInsights.Field.cost_per_unique_action_type,
        AdsInsights.Field.cost_per_thruplay,
        AdsInsights.Field.cost_per_outbound_click,
        AdsInsights.Field.actions,
        AdsInsights.Field.cost_per_action_type
    ]

    account_fields = [
        AdsInsights.Field.account_id,
        AdsInsights.Field.account_name
    ]

    campaign_fields = [
        AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name
    ]

    ad_fields = [
        AdsInsights.Field.ad_id,
        AdsInsights.Field.date_start,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.spend,
        AdsInsights.Field.actions,
        AdsInsights.Field.frequency
    ]

    meta_insights = MetaInsights(
        account=my_account,
        fields=ad_fields,
        level="ad"
        )

    #meta_insights.insert_daily_ad_series()
    #meta_insights.insert_daily_age_gender()
    meta_insights.insert_daily_country()
























































