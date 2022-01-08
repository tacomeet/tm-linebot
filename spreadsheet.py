import pandas as pd
# from gspread_dataframe import set_with_dataframe


def get_worksheet_as_dataframe(worksheet):
    df = pd.DataFrame(worksheet.get_all_values())
    df.columns = list(df.loc[0, :])
    df.drop(0, inplace=True)
    df.set_index('id', inplace=True)
    return df
