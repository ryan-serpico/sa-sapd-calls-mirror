import json
import os

import pandas as pd
import requests

# If output folder does not exist, create it
if not os.path.exists('output'):
    os.makedirs('output')


def get_data(url):
    print('Requesting data ...')

    r = requests.get(url)
    data = r.json()['features']
    return data

data = get_data('https://services.arcgis.com/g1fRTDLeMgspWrYp/arcgis/rest/services/CFS_SAPD_7Days/FeatureServer/0//query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=*&returnGeometry=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=')

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

# Drop the first two columns
df = df.drop(['OBJECTID', 'CADID', 'ResponseDateText'], axis=1)

# Reorder the columns
df = df[['Date', 'Time', 'Address', 'Zipcode', 'Category', 'ProblemType', 'PatrolDistrict', 'Substation', 'IncidentNumber', 'LAT', 'LON', 'ResponseDate', 'URL', 'Color', 'About']]

# Save the dataframe to a csv file
df.to_csv('output/data.csv', index=False)
