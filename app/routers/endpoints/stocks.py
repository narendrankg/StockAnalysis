from fastapi import APIRouter, Depends
import pandas as pd
from typing_extensions import Annotated
from .token import oauth2_scheme, decode_access_token

router = APIRouter()

@router.get("/")
async def root(year, col, token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_access_token(token=token)
    print(user)
    acceptable_cols = ['Open','High','Low','Close']
    if not col or col not in acceptable_cols:
        return {"error":"Unknown col"}
    if not year:
        return {"error":"Unknown year"}
    year_to_check = int(year)
    column_to_check = col
    df=pd.read_csv("C:/Users/Narendra/Documents/LambdaBuild/app/indexData.csv",parse_dates=['Date'], index_col="Date")
    
    df_year_col = df.loc[df.index.year == year_to_check, ["Index", column_to_check]]

    # Group by stock and calculate the mean for the selected column
    df_year_col_mean = df_year_col.groupby("Index").mean()

    # Group by stock and calculate the max for the selected column
    df_year_col_max = df_year_col.groupby("Index").max()

    # Group by stock and calculate the min for the selected column
    df_year_col_min = df_year_col.groupby("Index").min()

    # Find the stock with the highest average value for the specified column and year
    best_stock_mean = df_year_col_mean[column_to_check].idxmax()
    # Find the stock with the highest max value for the specified column and year
    best_stock_max = df_year_col_max[column_to_check].idxmax()
    # Find the stock with the highest min value for the specified column and year
    best_stock_min = df_year_col_min[column_to_check].idxmax()
    return {"message": "Get Stocks Analysis!",
            "stocks_list_max": best_stock_max,
            "stocks_list_min": best_stock_min,
            "stocks_list_avg": best_stock_mean}