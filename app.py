import os
from datetime import datetime

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

def population_data_import():
    population_df = pd.read_csv('input/ACSDT5Y2020.B01003-Data.csv', skiprows=1)

    # Drop the first column by index
    population_df = population_df.drop(population_df.columns[0], axis=1)

    # Drop the last three columns by index
    population_df = population_df.drop(population_df.columns[-4:], axis=1)

    # Rename the columns
    population_df.columns = ['Zipcode', 'Population']

    # Remove "ZCTA5 " from the Zipcode column
    population_df['Zipcode'] = population_df['Zipcode'].str.replace('ZCTA5 ', '')

    return population_df

def data_analysis():
    '''
    This function performs some basic analysis on the data.
    '''
    print('👉 Performing data analysis ...')

    population_df = population_data_import()

    # Loop through every csv in the output directory, ignore folders
    for file in os.listdir('output'):
        if os.path.isfile(os.path.join('output', file)):
            if file == '.DS_Store':
                continue

            # Go through the "Date" column in each file to check if it contains the last date of the month
            df = pd.read_csv(f'output/{file}')

            # Extract the YY and MM from the filename
            year = file.split('-')[0]
            month = int(file.split('-')[1].split('.')[0])

            # Check to see if the analysis file already exists in the analysis directory. If it does, skip it. If it doesn't, create it. This is to prevent the script from overwriting the analysis file each time it runs. The analysis file will only be updated once a month.
            if not os.path.exists(f'output/analysis/{year}-{month}-analysis.csv'):
                print(f'👉 {year}-{month}-analysis.csv does not exist!')
            else:
                print(f'👉 {year}-{month}-analysis.csv already exists! Skipping ...')
                continue

            # Get the current MM and YY
            current_month = int(datetime.now().month)
            df['Date'] = pd.to_datetime(df['Date'])
            df['LastDayOfMonth'] = df['Date'].dt.is_month_end

            if month + 1 == current_month and df['LastDayOfMonth'].any():
                print(f'👉 Analyzing {file} ...')

                # If the data in the zipcode column has more than 5 digits, remove the hyphen and everything after it
                df['Zipcode'] = df['Zipcode'].str.split('-', expand=True)[0]

                # Count how many times each ZIP code appears in the "Zipcode" column
                zip_counts_df = df['Zipcode'].value_counts().to_frame().reset_index().rename(columns={'index': 'Zipcode', 'Zipcode': 'Count'})

                # Merge the zip_counts_df dataframe with the population_df dataframe
                zip_counts_df = zip_counts_df.merge(population_df, on='Zipcode', how='left')

                # Reorder the columns
                zip_counts_df = zip_counts_df[['Zipcode', 'Population', 'Count']]

                # Calculate the incidents per 1,000 people and round to one decimal place
                zip_counts_df['IncidentsPer1000'] = round(zip_counts_df['Count'] / zip_counts_df['Population'] * 1000, 1)
                
                # Sort the dataframe by the "Count" column
                zip_counts_df = zip_counts_df.sort_values(by='IncidentsPer1000', ascending=False)

                # Remove any rows where the "IncidentsPer1000" column is NaN
                zip_counts_df = zip_counts_df.dropna(subset=['IncidentsPer1000'])

                # Find the most common "ProblemType" for each ZIP code and the number of times it appears (NOTE: Review how copilot is doing this. You verified that it's accurate on Thursday, October 27, 2022.)
                zip_problem_df = df.groupby(['Zipcode', 'ProblemType']).size().to_frame('Count').reset_index().sort_values(by=['Zipcode', 'Count'], ascending=False).groupby('Zipcode').head(1)

                # Merge the zip_problem_df dataframe with the zip_counts_df dataframe
                zip_analysis = zip_counts_df.merge(zip_problem_df, on='Zipcode', how='left')

                # Rename "Count_x" to "Count" and "Count_y" to "ProblemCount"
                zip_analysis = zip_analysis.rename(columns={'Count_x': 'Count', 'Count_y': 'ProblemCount'})

                zip_analysis.to_csv(f'output/analysis/{year}-{month}-analysis.csv', index=False)

                print(f'👉 {year}-{month}-analysis.csv created!')


compile_data()

data_analysis()

