import pandas as pd
from datetime import datetime, time
import xlsxwriter

# df = pd.read_csv('data.csv')
df = pd.read_excel('data2.xlsx')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df = df.sort_values(by='DateTime', ascending=False)
df['Date'] = df['DateTime'].dt.date
df['Time'] = df['DateTime'].dt.time




def createResult():

    new_df = pd.DataFrame()
    date_counts_dict = countData()

    for date, count in date_counts_dict.items():
        filtered_df = filter_df(date)
        new_filtered_df = processEachColumnToDF(filtered_df)
        new_df = constructNewDF(new_df, new_filtered_df)


    new_df.style.set_properties(**{'text-align': 'center'})

    return new_df

def countData():
 
    date_counts = df['Date'].value_counts().sort_index(ascending=False)
    date_counts_dict = date_counts.to_dict()
    return date_counts_dict

def filter_df(specific_date):

    filtered_df = df[df['DateTime'].dt.date == specific_date]
    filtered_df = filtered_df[['Date', 'Time']]
    filtered_df['Each'] = ''
    filtered_df['Daily total'] = ''

    return filtered_df



def constructNewDF(new_df, filtered_df):
    return pd.concat([new_df, filtered_df], ignore_index=True)




def processEachColumnToDF(filtered_df):
    timestamp_zero = 0
    count = len(filtered_df) 
    for i in range(0, count - 1):
        if i % 2 == 0:
            time1 = filtered_df['Time'].iloc[i]  
            time2 = filtered_df['Time'].iloc[i+1]

            time1 = time_to_seconds(time1)
            time2 = time_to_seconds(time2)

            time_diff = time1 - time2
            timestamp_zero += time_diff

            filtered_df['Each'].iloc[i] = seconds_to_time(time_diff) 
  

    if count % 2 == 0:
        filtered_df['Daily total'].iloc[0] = seconds_to_time(timestamp_zero) 
    else:
        filtered_df['Daily total'] = 'Error'


    return filtered_df

def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second



# Convert the time difference from seconds to hours, minutes, and seconds
def seconds_to_hms(seconds):
    hours, remainder = divmod(abs(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)

# Convert the time difference to a datetime.time object
def seconds_to_time(seconds):
    hours, minutes, seconds = seconds_to_hms(seconds)
    hours = hours % 24
    
    return time(hour=hours, minute=minutes, second=seconds)




def convertToDateTime(time_diff):
    seconds = time_diff.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_diff_as_time = datetime.time(datetime(1, 1, 1, int(hours), int(minutes), int(seconds)))


    return time_diff_as_time







filename = 'output.xlsx'
outputDF = createResult()
outputDF = outputDF.sort_values(by=['Date', 'Time'])
outputDF.to_excel(filename, index=False, engine='openpyxl')
