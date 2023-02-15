from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR,MEDIUMINT,DATE,BIGINT,FLOAT

Base = declarative_base()

class Accounts(Base):
    __tablename__ = "accounts"
    account_id = Column(VARCHAR(250), primary_key=True,nullable=False)
    account_name = Column(VARCHAR(250),nullable=False)
    account_currency = Column(VARCHAR(3),nullable=False)
    campaigns = relationship("Campaigns",back_populates="accounts")


class Campaigns(Base):
    __tablename__ = "campaigns"
    campaign_id = Column(VARCHAR(250),primary_key=True,nullable=False)
    account_id = Column(VARCHAR(250),ForeignKey("accounts.account_id"),nullable=False)
    campaign_name = Column(VARCHAR(45),nullable=False)
    accounts = relationship("Accounts",back_populates = "campaigns")
    adsets = relationship("Adsets",back_populates = "campaigns")


class Adsets(Base):
    __tablename__ = "adsets"
    adset_id = Column(VARCHAR(250),primary_key=True,nullable=False)
    campaign_id = Column(VARCHAR(250),ForeignKey("campaigns.campaign_id"),nullable=False)
    adset_name = Column(VARCHAR(45),nullable=False)
    campaigns = relationship("Campaigns",back_populates="adsets")
    ads = relationship("Ads",back_populates="adsets")



class Ads(Base):
    __tablename__ = "ads"
    ad_id = Column(VARCHAR(45),primary_key=True,nullable=False)
    adset_id = Column(VARCHAR(150),ForeignKey("adsets.adset_id"),nullable=False)
    ad_name = Column(VARCHAR(250),nullable=False)
    adsets = relationship("Adsets",back_populates = "ads")
    ad_series = relationship("AdSeries",back_populates="ads")

class AdSeries(Base):
    __tablename__ = "ad_series"
    id = Column(MEDIUMINT,primary_key=True,nullable=False)
    ad_id = Column(VARCHAR(250),ForeignKey("ads.ad_id"),nullable=False)
    date = Column(DATE,nullable=False)
    impressions = Column(BIGINT,nullable=False)
    clicks = Column(BIGINT,nullable=False)
    total_spend = Column(FLOAT,nullable=False)
    video_view = Column(BIGINT,nullable=False)
    comment = Column(BIGINT,nullable=False)
    link_click = Column(BIGINT,nullable=False)
    post_reaction = Column(BIGINT,nullable=False)
    landing_page_view = Column(BIGINT,nullable=False)
    post_engagement = Column(BIGINT,nullable=False)
    leadgen_grouped = Column(BIGINT,nullable=False)
    lead = Column(BIGINT,nullable=False)
    page_engagement = Column(BIGINT,nullable=False)
    onsite_conversion_post_save = Column(BIGINT,nullable=False)
    onsite_conversion_lead_grouped = Column(BIGINT,nullable=False)
    offsite_conversion_fb_pixel_lead = Column(BIGINT,nullable=False)
    frequency = Column(FLOAT,nullable=False)
    ads = relationship("Ads",back_populates="ad_series")

