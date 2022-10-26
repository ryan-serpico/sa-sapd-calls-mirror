import json
import os

import pandas as pd
import requests

# If output folder does not exist, create it
if not os.path.exists('output'):
    os.makedirs('output')

def get_data(url):
    '''
    This function reaches out to SAPD's arcgis server and returns the data.
    '''
    r = requests.get(url)
    data = r.json()['features']
    return data

def transform_data(data, i):
    '''
    This function loads the json response from SAPD's arcgis server into a dataframe. It also breaks apart the ResponseDateText field into separate columns for the date and time. Finally, it rearranges the columns in order of usefulness. 
    '''
    # Create a dataframe
    df = pd.DataFrame()

    # Add each item from the data to the dataframe
    for item in data:
        item_df = pd.DataFrame(item['attributes'], index=[0])
        df = pd.concat([df, item_df])

    # Pull the date from the ResponseDateText column and put it in a new column
    df['Date'] = df['ResponseDateText'].str.split(' ', expand=True)[0]

    # Pull the time from the ResponseDateText column and put it in a new column
    df['Time'] = df['ResponseDateText'].str.split(' ', expand=True)[1] + ' ' + df['ResponseDateText'].str.split(' ', expand=True)[2]

    # Extract the date parts from the Date column
    df['Year'] = df['Date'].str.split('/', expand=True)[2]
    df['Month'] = df['Date'].str.split('/', expand=True)[0]
    # Remove leading zeros from the Month column
    df['Month'] = df['Month'].str.lstrip('0')


    # Drop the first two columns
    df = df.drop(['OBJECTID', 'CADID', 'ResponseDateText'], axis=1)

    # Reorder the columns
    df = df[['Date', 'Time', 'Address', 'Zipcode', 'Category', 'ProblemType', 'PatrolDistrict', 'Substation', 'IncidentNumber', 'LAT', 'LON', 'ResponseDate', 'URL', 'Color', 'About', 'Year', 'Month']]

    return df

def compile_data():
    '''
    This function pages through the SAPD's arcgis server responses and compiles all the data into a single dataframe. It then checks to see which records don't exist in the archive and subsequently adds them to it.
    '''
    new_data_df = pd.DataFrame()

    # Create a for loop that starts at 0 and goes to 20000, iterating by 2000 each time
    for i in range(0, 200000, 2000):
        data = get_data('https://services.arcgis.com/g1fRTDLeMgspWrYp/arcgis/rest/services/CFS_SAPD_7Days/FeatureServer/0//query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=*&returnGeometry=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset={}&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token='.format(i))

        try:
            partial_data = transform_data(data, i)
            new_data_df = pd.concat([new_data_df, partial_data])
        except Exception as e:
            print(e)
            break
    
    for month in new_data_df['Month'].unique():
        for year in new_data_df['Year'].unique():
            print(f'👉 Checking for new data for {year}-{month}.csv ...')
            try:
                # if the file doesn't already exist, create it
                if not os.path.exists(f'output/{year}-{month}.csv'):
                    new_data_df[(new_data_df['Month'] == month) & (new_data_df['Year'] == year)].to_csv(f'output/{year}-{month}.csv', index=False)

                archive = pd.read_csv(f'output/{year}-{month}.csv')
                print(f'👉 Merging and deduping {year}-{month}.csv ...')
                appended_df = pd.concat([archive, new_data_df[(new_data_df['Month'] == month) & (new_data_df['Year'] == year)]]).drop_duplicates(subset='IncidentNumber', keep='first')
                print(f'👉 Updating {year}-{month}.csv')
                appended_df.to_csv(f'output/{year}-{month}.csv', index=False)
            except Exception as e:
                print(e)
                pass

def breakup_archive(data):
    '''
    This function breaks up the archive into separate csv files for each month each year.
    '''
    print('👉 Breaking up archive ...')
    df = pd.read_csv(data)

    # Extract the date parts from the Date column
    df['Year'] = df['Date'].str.split('/', expand=True)[2]
    df['Month'] = df['Date'].str.split('/', expand=True)[0]

    # Remove leading zeros from the Month column
    df['Month'] = df['Month'].str.lstrip('0')

    for month in df['Month'].unique():
        for year in df['Year'].unique():
            df[(df['Month'] == month) & (df['Year'] == year)].to_csv(f'output/{year}-{month}.csv', index=False)

compile_data()

