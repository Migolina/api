import pandas as pd
import numpy as np

class Insights:
    def __init__(self,account,since,until,levels,fields=None):
        self.account = account
        self.levels = levels
        self.since = since
        self.until = until
        self.fields = fields

        self.time_range = dict(since=self.since, until=self.until)

    def get_insights(self):
        insight_levels = {"ad":[],"adset":[],"campaign":[],"account":[]}
        for level in self.levels:
            params = {
                "level":level,
                "time_range":self.time_range
            }

            insights = self.account.get_insights(params=params,fields=self.fields)

            insight_levels[level] = insights

        return insight_levels

    def convert_fields(self,df,integer_fields,float_fields,date_fields):
        df[integer_fields] = df[integer_fields].astype(int)
        df[float_fields] = df[float_fields].astype(float)
        df[date_fields] = df[date_fields].apply(lambda x: pd.to_datetime(x, errors="coerce", format="%Y-%m-%d"))

        return df

    def save_dataframe(self):
        insight_levels = self.get_insights()

        integer_fields = ["clicks", "impressions", "inline_link_clicks", "inline_post_engagement", "reach"]

        float_fields = ["cost_per_inline_link_click", "cost_per_inline_post_engagement", "cost_per_unique_click",
                        "cost_per_unique_inline_link_click", "cpc", "cpp", "cpm", "ctr", "frequency",
                        "inline_link_click_ctr",
                        "social_spend", "spend"]

        date_fields = ["date_start", "date_stop"]

        dataframes = []
        for key in insight_levels.keys():
            index = list(range(len(insight_levels[key])))
            df = pd.DataFrame(insight_levels[key],index=index)

            integer_fields = list(set(df.columns) & set(integer_fields))
            float_fields = list(set(df.columns) & set(float_fields))

            #fix datatypes
            df = self.convert_fields(df,integer_fields,float_fields,date_fields)

            dataframes.append(df)

        return dataframes

    def save_csv(self):
        dataframe = self.save_dataframe()

        for name,df in zip(["ad_level","adset_level","campaign_level","account_level"],dataframe):
            df.to_csv(f"data/{name}.csv",index=False)
            msg = f"{name}.csv succesfully saved under the data directory"
            print(msg)

























