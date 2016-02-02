# Lesson 2 Notes:

import pandas
def add_full_name(path_to_csv, path_to_new_csv):
    #Assume you will be reading in a csv file with the same columns that the
    #Lahman baseball data set has -- most importantly, there are columns
    #called 'nameFirst' and 'nameLast'.
    #1) Write a function that reads a csv
    #located at "path_to_csv" into a pandas dataframe and adds a new column
    #called 'nameFull' with a player's full name.
    #
    #For example:
    #   for Hank Aaron, nameFull would be 'Hank Aaron', 
	#
	#2) Write the data in the pandas dataFrame to a new csv file located at
	#path_to_new_csv

    #WRITE YOUR CODE HERE
    data = pandas.read_csv(path_to_csv)
    data['nameFull'] = data['nameFirst'] + ' ' + data['nameLast']
    data.to_csv(path_to_new_csv)
    # print data.head()
if __name__ == "__main__":
    # For local use only
    # If you are running this on your own machine add the path to the
    # Lahman baseball csv and a path for the new csv.
    # The dataset can be downloaded from this website: http://www.seanlahman.com/baseball-archive/statistics
    # We are using the file Master.csv
    path_to_csv = ""
    path_to_new_csv = ""
    add_full_name(path_to_csv, path_to_new_csv)

# output:
  0,Hank,Aaron,Hank Aaron
  1,Tommie,Aaron,Tommie Aaron
  2,Don,Aase,Don Aase
  3,Andy,Abad,Andy Abad
  4,John,Abadie,John Abadie
  5,Ed,Abbaticchio,Ed Abbaticchio
  6,Bert,Abbey,Bert Abbey

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Lesson 2 cont... ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
import pandasql

def select_first_50(filename):
    # Read in our aadhaar_data csv to a pandas dataframe.  Afterwards, we rename the columns
    # by replacing spaces with underscores and setting all characters to lowercase, so the
    # column names more closely resemble columns names one might find in a table.
    aadhaar_data = pandas.read_csv(filename)
    aadhaar_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)

    # Select out the first 50 values for "registrar" and "enrolment_agency"
    # in the aadhaar_data table using SQL syntax. 
    #
    # Note that "enrolment_agency" is spelled with one l. Also, the order
    # of the select does matter. Make sure you select registrar then enrolment agency
    # in your query.
    #
    # You can download a copy of the aadhaar data that we are passing 
    # into this exercise below:
    # https://www.dropbox.com/s/vn8t4uulbsfmalo/aadhaar_data.csv
    q = """
    select "registrar", "enrolment_agency" from aadhaar_data
    limit 50;
    """

    #Execute your SQL command against the pandas frame
    aadhaar_solution = pandasql.sqldf(q.lower(), locals())
    return aadhaar_solution   

# output:
  0,Allahabad Bank,Tera Software Ltd
  1,Allahabad Bank,Tera Software Ltd
  2,Allahabad Bank,Vakrangee Softwares Limited
  3,Allahabad Bank,Vakrangee Softwares Limited
  4,Allahabad Bank,Vakrangee Softwares Limited
  5,Allahabad Bank,Vakrangee Softwares Limited 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Lesson 2 cont... ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
import pandasql

def aggregate_query(filename):
    # Read in our aadhaar_data csv to a pandas dataframe.  Afterwards, we rename the columns
    # by replacing spaces with underscores and setting all characters to lowercase, so the
    # column names more closely resemble columns names one might find in a table.
    
    aadhaar_data = pandas.read_csv(filename)
    aadhaar_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)

    # Write a query that will select from the aadhaar_data table how many men and how 
    # many women over the age of 50 have had aadhaar generated for them in each district.
    # aadhaar_generated is a column in the Aadhaar Data that denotes the number who have had
    # aadhaar generated in each row of the table.
    #   
    q = """
    SELECT
    gender, district, sum(aadhaar_generated)
    FROM
    aadhaar_data
    WHERE
    age > 50
    GROUP BY
    gender, district
    """
    # Execute your SQL command against the pandas frame
    aadhaar_solution = pandasql.sqldf(q.lower(), locals())
    return aadhaar_solution
# output:
Good job! Your code worked perfectly.


    gender                    district  sum(aadhaar_generated)
0        F                  Ahmadnagar                      45
1        F                 Ahmed Nagar                       0
2        F                   Ahmedabad                       1
3        F                       Ajmer                      27
4        F                       Akola                       5
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Lesson 2 cont... ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import json
import requests
import pprint

def api_get_request(url):
    # In this exercise, you want to call the last.fm API to get a list of the
    # top artists in Spain. The grader will supply the URL as an argument to
    # the function; you do not need to construct the address or call this
    # function in your grader submission.

    data = requests.get(url).text
    parsed = json.loads(data)
    print parsed['topartists']['artist'][2]['name']
    
    print json.dumps(parsed, indent=4, sort_keys=True)

    return parsed['topartists']['artist'][0]['name']
# output:
Arctic Monkeys
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Lesson 2 cont... ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
import numpy

def imputation(filename):
    # Pandas dataframes have a method called 'fillna(value)', such that you can
    # pass in a single value to replace any NAs in a dataframe or series. You
    # can call it like this: 
    #     dataframe['column'] = dataframe['column'].fillna(value)
    #
    # Using the numpy.mean function, which calculates the mean of a numpy
    # array, impute any missing values in our Lahman baseball
    # data sets 'weight' column by setting them equal to the average weight.

    baseball = pandas.read_csv(filename)
    # isnull() returns boolean on df col for NaN or non NaN. sum() counts & returns and int.
    print baseball['weight'].isnull().sum()
    baseball['weight'] = baseball['weight'].fillna(numpy.mean(baseball['weight']))
    print baseball['weight'].isnull().sum()
    return baseball
#output: 
43
0
Good job! Your imputation worked perfectly.
The following is the output by your program:

,nameFirst,nameLast,weight
0,Hank,Aaron,180.0
1,Tommie,Aaron,190.0
2,Don,Aase,190.0
3,Andy,Abad,184.0
4,John,Abadie,192.0
5,Ed,Abbaticchio,170.0
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PROBLEM SET 2.1:

import pandas
import numpy
import pandasql


def num_rainy_days(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - a count of the number of days in the dataframe where
    the rain column is equal to 1 (i.e., the number of days it
    rained).
                https://dev.mysql.com/doc/refman/5.1/en/counting-rows.html
    You might also find that interpreting numbers as integers or floats may not
    work initially.  In order to get around this issue, it may be useful to cast
    these numbers as integers.  This can be done by writing cast(column as integer).
    So for example, if we wanted to cast the maxtempi column as an integer, we would actually
    write something like where cast(maxtempi as integer) = 76, as opposed to simply 
    where maxtempi = 76.
    '''
    weather_data = pandas.read_csv(filename)
    #print weather_data.head()
    #print weather_data.columns.values
    #print numpy.sum(weather_data['rain'] > 0)
    q = """
    SELECT
    COUNT(*)
    FROM
    weather_data
    WHERE
    rain == 1
    """
    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days

# output:
   count(*)
0        10
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas
import pandasql


def max_temp_aggregate_by_fog(filename):

    weather_data = pandas.read_csv(filename)
    #print weather_data.columns.values
    #print weather_data['maxtempi'].head()
    q = """
    SELECT
    fog, max(maxtempi)
    FROM
    weather_data
    GROUP BY
    fog
    """
    #Execute your SQL command against the pandas frame
    foggy_days = pandasql.sqldf(q.lower(), locals())
    return foggy_days
# Output:
   fog  max(maxtempi)
0    0             86
1    1             81
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
import pandasql

def avg_weekend_temperature(filename):
    '''
    The SQL query should return one column and
    one row - the average meantempi on days that are a Saturday
    or Sunday (i.e., the the average mean temperature on weekends).
    The dataframe will be titled 'weather_data' and you can access
    the date in the dataframe via the 'date' column.
    
    Also, you can convert dates to days of the week via the 'strftime' keyword in SQL.
    For example, cast (strftime('%w', date) as integer) will return 0 if the date
    is a Sunday or 6 if the date is a Saturday.
    '''
    weather_data = pandas.read_csv(filename)
    #print weather_data.columns.values
    
    q = """
    SELECT
    avg(cast(meantempi as integer))
    FROM
    weather_data
    WHERE
    cast(strftime('%w', date) as integrer) == 0 or cast(strftime('%w', date) as integer) == 6
    """
    
    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends
# Output:
   avg(cast(meantempi as integer))
0                        65.111111
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.4 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
import pandasql

def avg_min_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data. More specifically you want to find the average
    minimum temperature (mintempi column of the weather dataframe) on 
    rainy days where the minimum temperature is greater than 55 degrees.

    '''
    weather_data = pandas.read_csv(filename)

    q = """
    SELECT
    avg(cast(mintempi as integer))
    FROM
    weather_data
    WHERE
    cast(mintempi as integer) > 55 and rain = 1
    """
    
    #Execute your SQL command against the pandas frame
    avg_min_temp_rainy = pandasql.sqldf(q.lower(), locals())
    return avg_min_temp_rainy
# Output:
   avg(cast(mintempi as integer))
0                           61.25
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.5 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import csv
f_in = open('turnstile_110528.txt', 'r')
f_out = open('kyle_sol_turnstile_110528.csv', 'w')
reader_in = csv.reader(f_in, delimiter=',')
writer_out = csv.writer(f_out, delimiter=',')
for line in reader_in:
    count = 0
    # number of unique data rows in each line
    unique_blocks = (len(line)-3)/5
    # these three items will go in front of every unique row
    same_first_blocks = line[:3]
    # value to move through list in increments of 5
    start = len(same_first_blocks)
    while count != unique_blocks:
        writer_out.writerow(same_first_blocks + line[start:start+5])
        count += 1
        start += 5
f_in.close()
f_out.close()
# Output: csv file
A002,R051,02-00-00,05-21-11,00:00:00,REGULAR,003169391,001097585
A002,R051,02-00-00,05-21-11,04:00:00,REGULAR,003169415,001097588
A002,R051,02-00-00,05-21-11,08:00:00,REGULAR,003169431,001097607
A002,R051,02-00-00,05-21-11,12:00:00,REGULAR,003169506,001097686
A002,R051,02-00-00,05-21-11,16:00:00,REGULAR,003169693,001097734
A002,R051,02-00-00,05-21-11,20:00:00,REGULAR,003169998,001097769
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.6 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import csv
def create_master_turnstile_file(filenames, output_file):
    with open(output_file, 'w') as master_file:
       master_file.write('C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')
       writer = csv.writer(master_file)
       for filename in filenames:
           with open(filename, 'rb') as f:
               reader = csv.reader(f)
               for row in reader:
                   s1 = []
                   s1 = row[0:8]
                   writer.writerow(s1)
# Output:
C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn
A002,R051,02-00-00,05-21-11,00:00:00,REGULAR,003169391,001097585
A002,R051,02-00-00,05-21-11,04:00:00,REGULAR,003169415,001097588
A002,R051,02-00-00,05-21-11,08:00:00,REGULAR,003169431,001097607
A002,R051,02-00-00,05-21-11,12:00:00,REGULAR,003169506,001097686
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.7 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd

def filter_by_regular(filename):
    # note using df.from_csv vs. df_read_csv  watch Index.. -> index_col = None
    turnstile_data = pd.DataFrame.from_csv(filename, index_col = None)
    turnstile_data = turnstile_data[turnstile_data['DESCn'] == 'REGULAR']
    return turnstile_data
# Output:  pandasd dataframe

       C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn
0     A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151
1     A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159
2     A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177
3     A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.8 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
def get_hourly_entries(df):
    df['ENTRIESn_hourly'] = df['ENTRIESn'] - df['ENTRIESn'].shift()
    df['ENTRIESn_hourly'].fillna(1, inplace=True)
    return df
# .shift(1) changes the index of the row or column [depending on axis = 0 or 1] value to the one before
# ENTRIESn 1 - 0 = 23 which is put for hourly  
# Output: Examples of what your dataframe should look like at the end of this exercise:
    
           C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn  ENTRIESn_hourly
    0     A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151                1
    1     A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159               23
    2     A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177               18
    3     A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231               71
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.9 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas
def get_hourly_exits(df):   
    df['EXITSn_hourly'] = df['EXITSn'] - df['EXITSn'].shift(1)
    df['EXITSn_hourly'].fillna(0, inplace = True)
    return df
# Output: 
 Unnamed: 0   C/A  UNIT       SCP     DATEn     TIMEn    DESCn  ENTRIESn    EXITSn  ENTRIESn_hourly  EXITSn_hourly
    0     0  A002  R051  02-00-00  05-01-11  00:00:00  REGULAR   3144312   1088151                0              0
    1     1  A002  R051  02-00-00  05-01-11  04:00:00  REGULAR   3144335   1088159               23              8
    2     2  A002  R051  02-00-00  05-01-11  08:00:00  REGULAR   3144353   1088177               18             18
    3     3  A002  R051  02-00-00  05-01-11  12:00:00  REGULAR   3144424   1088231               71             54
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.10 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd
def time_to_hour(time):
    '''
    Given an input variable time that represents time in the format of:
    "00:00:00" (hour:minutes:seconds)
    Write a function to extract the hour part from the input variable time
    and return it as an integer. For example:
        1) if hour is 00, your code should return 0
        2) if hour is 01, your code should return 1
        3) if hour is 21, your code should return 21
    '''
    #print time, type(time)
    hour = int(time[:2])
    #print hour, type(hour)
    return hour
# Output: 
00:00:00 <type 'str'>
0 <type 'int'>
04:00:00 <type 'str'>
4 <type 'int'>
08:00:00 <type 'str'>
8 <type 'int'>
12:00:00 <type 'str'>
12 <type 'int'>
16:00:00 <type 'str'>
16 <type 'int'>
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Problem Set 2.11 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import datetime
def reformat_subway_dates(date):
    # as-is: month-day-year
    # to-be: year-month-day
    old_date = datetime.strptime(date, "%m-%d-%y")
    new_date = datetime.strftime(old_date, '%Y-%m-%d')
    date_formatted = new_date
    return date_formatted