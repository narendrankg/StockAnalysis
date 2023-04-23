from fastapi import APIRouter, Depends
import pandas as pd
from typing_extensions import Annotated
from .authentication import oauth2_scheme, decode_access_token
import requests
#import json
#import boto3

router = APIRouter()

@router.get("/")
async def root(year, col, token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_access_token(token=token)
    acceptable_cols = ['Open','High','Low','Close']
    if not col or col not in acceptable_cols:
        return {"error":"Unknown col"}
    if not year:
        return {"error":"Unknown year"}
    year_to_check = int(year)
    column_to_check = col
    print(f'{user} requested details for given year: {year_to_check} column: {column_to_check}')
    params = {}
    params['year_to_check'] = year_to_check
    params['column_to_check'] = col
    get_response_data = {}
    try:
        # code to external lambda function api to get the required data this will give us flexibility in case of the datasource changes. then we need not to change in out application logic
        get_response = requests.get("https://f5cihzh66dizaia2x4agwiz7ee0dywly.lambda-url.us-east-1.on.aws/", params=params)
        print("API response status code: %s" % get_response.status_code)
        # get_response_data = json.loads(get_response.text)
        # return get_response_data
        # Forcefully raising exception here as i was facing issue working with pandas on aws lambda. else will return successful response from here.
        raise Exception("Forcefully raised Error")
    except Exception as e:
        print("Exception occured" + str(e))

        # following code will be part of aws lambda. As ideally we need to raise error with relevant message, in case of failure from downsteam aws lambda."
        ###############start################
        #Code in case we want to read the file from S3
        #s3_client = boto3.client("s3")
        #S3_BUCKET_NAME = 'narendra-test-bucket-stock-ai'
        #object_key = "indexData.csv"  # replace object key
        #file_data = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_key)["Body"]
        
        #Code in case we want to read the locally available file
        df=pd.read_csv("./indexData.csv", parse_dates=['Date'], index_col="Date")
        # filter Column and Year related data in seperate data frame
        df_year_col = df.loc[df.index.year == year_to_check, ["Index", column_to_check]]
        # calculate the mean for the selected column
        best_stock_mean = df_year_col[column_to_check].mean()
        # Find the stock with the highest max value for the specified column and year
        best_stock_max = df_year_col.loc[df_year_col[column_to_check].idxmax(), 'Index']
        # Find the stock with the highest min value for the specified column and year
        best_stock_min = df_year_col.loc[df_year_col[column_to_check].idxmin(), 'Index']
        return {"min_price_stock": best_stock_max,
                "max_price_stock": best_stock_min,
                "average_price_of_the_year": best_stock_mean}
        ###############end################
    return get_response_data
