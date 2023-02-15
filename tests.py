from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from dotenv import load_dotenv
import os

from facebook.insights import Insights
from meta.meta_insights import MetaInsights

load_dotenv()

app_id = str(os.getenv("APP_ID"))
app_secret = str(os.getenv("APP_SECRET"))
access_token = str(os.getenv("ACCESS_TOKEN"))
account = str(os.getenv("ACCOUNT"))

FacebookAdsApi.init(app_id, app_secret, access_token)
my_account = AdAccount(account)

# queries
from mysql_orm.models import Accounts,Campaigns
from mysql_orm import session
from sqlalchemy import select

# add new account

new_account = Campaigns(account_id="525510428828068",
                        campaign_id = "test",
                        campaign_name = "test")


session.add(new_account)
session.commit()

stmt = select(Campaigns)
result = session.execute(stmt)

for row in session.execute(stmt):
    print(row.Campaigns.campaign_name)









