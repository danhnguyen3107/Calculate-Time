import pandas as pd
from datetime import datetime, time


df = pd.read_csv('data.csv')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Date'] = df['DateTime'].dt.date
df['Time'] = df['DateTime'].dt.time




def createResult():

    new_df = pd.DataFrame()
    date_counts_dict = countData()

    for date, count in date_counts_dict.items():
        filtered_df = filter_df(date)
        if count % 2 == 0:
            new_filtered_df = processEachColumnToDF(filtered_df)
            new_df = constructNewDF(new_df, new_filtered_df)
        else:
            filtered_df['Each'] = 'Error day'
            new_df = constructNewDF(new_df, filtered_df)

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

    for i in range(0, len(filtered_df)):
        if i % 2 == 0:
            time1 = filtered_df['Time'].iloc[i]  
            time2 = filtered_df['Time'].iloc[i+1]

            time1 = time_to_seconds(time1)
            time2 = time_to_seconds(time2)

            time_diff = time1 - time2
            timestamp_zero += time_diff

            filtered_df['Each'].iloc[i] = seconds_to_time(time_diff) 
  

    
    filtered_df['Daily total'].iloc[0] = seconds_to_time(timestamp_zero) 


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
    # Ensure that hours are within 24-hour range
    hours = hours % 24
    return time(hour=hours, minute=minutes, second=seconds)




def convertToDateTime(time_diff):
    seconds = time_diff.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_diff_as_time = datetime.time(datetime(1, 1, 1, int(hours), int(minutes), int(seconds)))


    return time_diff_as_time




outputDF = createResult()

outputDF.to_excel('output.xlsx', index=False, engine='openpyxl')
