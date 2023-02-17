from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR,MEDIUMINT,DATE,BIGINT,FLOAT,SMALLINT

Base = declarative_base()

class Accounts(Base):
    __tablename__ = "accounts"
    account_id = Column(VARCHAR(250), primary_key=True,nullable=False)
    account_name = Column(VARCHAR(250))
    account_currency = Column(VARCHAR(3))
    campaigns = relationship("Campaigns",back_populates="accounts")


class Campaigns(Base):
    __tablename__ = "campaigns"
    campaign_id = Column(VARCHAR(250),primary_key=True,nullable=False)
    account_id = Column(VARCHAR(250),ForeignKey("accounts.account_id"),nullable=False)
    campaign_name = Column(VARCHAR(45))
    accounts = relationship("Accounts",back_populates = "campaigns")
    adsets = relationship("Adsets",back_populates = "campaigns")


class Adsets(Base):
    __tablename__ = "adsets"
    adset_id = Column(VARCHAR(250),primary_key=True,nullable=False)
    campaign_id = Column(VARCHAR(250),ForeignKey("campaigns.campaign_id"),nullable=False)
    adset_name = Column(VARCHAR(45))
    campaigns = relationship("Campaigns")
    ads = relationship("Ads",back_populates="adsets")


class Ads(Base):
    __tablename__ = "ads"
    ad_id = Column(VARCHAR(45),primary_key=True,nullable=False)
    adset_id = Column(VARCHAR(150),ForeignKey("adsets.adset_id"),nullable=False)
    ad_name = Column(VARCHAR(250))
    adsets = relationship("Adsets",back_populates = "ads")
    ad_series = relationship("AdSeries",back_populates="ads")
    age_and_gender = relationship("AgeGender",back_populates="ads")
    country = relationship("Country", back_populates="ads")

class AdSeries(Base):
    __tablename__ = "ad_series"
    id = Column(MEDIUMINT,primary_key=True,nullable=False)
    ad_id = Column(VARCHAR(250),ForeignKey("ads.ad_id"),nullable=False)
    date = Column(DATE)
    impressions = Column(BIGINT)
    clicks = Column(BIGINT)
    total_spend = Column(FLOAT)
    video_view = Column(BIGINT)
    comment = Column(BIGINT)
    link_click = Column(BIGINT)
    post_reaction = Column(BIGINT)
    landing_page_view = Column(BIGINT)
    post_engagement = Column(BIGINT)
    leadgen_grouped = Column(BIGINT)
    lead = Column(BIGINT)
    page_engagement = Column(BIGINT)
    onsite_conversion_post_save = Column(BIGINT)
    onsite_conversion_lead_grouped = Column(BIGINT)
    offsite_conversion_fb_pixel_lead = Column(BIGINT)
    frequency = Column(FLOAT)
    ads = relationship("Ads",back_populates="ad_series")

class AgeGender(Base):
    __tablename__ = "age_and_gender"
    id = Column(MEDIUMINT,primary_key=True,nullable=False)
    ad_id = Column(VARCHAR(18),ForeignKey("ads.ad_id"),nullable=False)
    age = Column(VARCHAR(5))
    gender = Column(VARCHAR(6))
    date = Column(DATE)
    impressions = Column(SMALLINT)
    clicks = Column(SMALLINT)
    total_spend = Column(FLOAT)
    video_view = Column(SMALLINT)
    comment = Column(SMALLINT)
    link_click = Column(SMALLINT)
    post_reaction = Column(SMALLINT)
    landing_page_view = Column(SMALLINT)
    post_engagement = Column(SMALLINT)
    leadgen_grouped = Column(SMALLINT)
    lead = Column(SMALLINT)
    page_engagement = Column(BIGINT)
    onsite_conversion_post_save = Column(SMALLINT)
    onsite_conversion_lead_grouped = Column(BIGINT)
    offsite_conversion_fb_pixel_lead = Column(BIGINT)
    frequency = Column(FLOAT)
    ads = relationship("Ads", back_populates="age_and_gender")


class Country(Base):
    __tablename__ = "country"
    id = Column(MEDIUMINT, primary_key=True, nullable=False)
    ad_id = Column(VARCHAR(18),ForeignKey("ads.ad_id"),nullable=False)
    country = Column(VARCHAR(5))
    date = Column(DATE)
    impressions = Column(SMALLINT)
    clicks = Column(SMALLINT)
    total_spend = Column(FLOAT)
    video_view = Column(SMALLINT)
    comment = Column(SMALLINT)
    link_click = Column(SMALLINT)
    post_reaction = Column(SMALLINT)
    landing_page_view = Column(SMALLINT)
    post_engagement = Column(SMALLINT)
    leadgen_grouped = Column(SMALLINT)
    lead = Column(SMALLINT)
    page_engagement = Column(BIGINT)
    onsite_conversion_post_save = Column(SMALLINT)
    onsite_conversion_lead_grouped = Column(BIGINT)
    offsite_conversion_fb_pixel_lead = Column(BIGINT)
    frequency = Column(FLOAT)
    ads = relationship("Ads", back_populates="country")







