import pandas as pd
import datetime
import glob
import os


def read_filter_df(f_ini=(datetime.datetime.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
                   f_fin=datetime.datetime.today().strftime('%Y-%m-%d'), path="../data/twitter_accounts/"):
    allfiles = glob.glob(path + "/*.csv")
    list_ = []

    for file_ in allfiles:
        df = pd.read_csv(file_, header=0, parse_dates=True, infer_datetime_format=True, index_col=0)
        screen_name = os.path.splitext(os.path.basename(file_))[0]
        df['screen_name'] = os.path.splitext(os.path.basename(file_))[0]
        df = df.loc[df['RT_temp'] == 0]

        df_dropped = df.drop(columns=["id_tweet", "id_twitter", "created_at", "in_reply_to_user_id",
                                      "in_reply_to_status_id", "in_reply_to_screen_name", "retweet_count",
                                      "favorite_count", "longitude", "latitude", "retweeted", "creation_date",
                                      "modification_date", "RT_temp", "is_retweeted"])

        df_time = df_dropped.loc[df['created_at_datetime'] > f_ini]
        df_time = df_time.loc[df['created_at_datetime'] < f_fin]
        df_empty = df_time.dropna(subset=['text'])
        df_clean = df_empty.drop_duplicates(subset="text", keep='last')
        list_.append(df_clean)
    df = pd.concat(list_, ignore_index=True)

    return df, f_ini, f_fin

