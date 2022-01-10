from gspread_dataframe import set_with_dataframe
import pandas as pd
from models.status_type import StatusType
from datetime import datetime

from models.user import User


def get_worksheet_as_dataframe(worksheet):
    df = pd.DataFrame(worksheet.get_all_values())
    df.columns = list(df.loc[0, :])
    df.drop(0, inplace=True)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)
    return df


def record_goal_rate(user: User, worksheet, df, goal):
    ss_type = user.get_session_type()
    elapsed_time = datetime.now() - user.get_session_start_timestamp()

    if ss_type == StatusType.CATCH_REC:
        rec_type = 'ロールモデルマッチング'
    elif ss_type in (
            StatusType.BN_CREATE,
            StatusType.BN_CREATE_TRACK1, StatusType.BN_CREATE_TRACK2, StatusType.BN_CREATE_TRACK3, StatusType.BN_CREATE_TRACK5):
        rec_type = '記事作成'

    df_goal_rate = pd.Series([rec_type, goal, elapsed_time.total_seconds()], index=['type', 'goal', 'elapsed_time [s]'])
    df = df.append(df_goal_rate, ignore_index=True)
    set_with_dataframe(worksheet, df)
