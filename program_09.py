#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:24:36 2020

@author: lu270
"""

import pandas as pd
import numpy as np

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=['1. No Data','2. Gross Error','3. Swapped','4. Range Fail'], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    
    # replace -999 by NaN
    DataDF=DataDF.replace(-999,np.nan)
    
    # Count number of replaced value
    ReplacedValuesDF.loc['1. No Data',:]=DataDF.isna().sum()

    return( DataDF, ReplacedValuesDF )
        
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    # check Gross Errors by given constrains
    DataDF['Precip'][(DataDF['Precip']<0)|(DataDF['Precip']>25)]=np.nan
    DataDF['Max Temp'][(DataDF['Max Temp']<-25)|(DataDF['Max Temp']>35)]=np.nan
    DataDF['Min Temp'][(DataDF['Min Temp']<-25)|(DataDF['Min Temp']>35)]=np.nan
    DataDF['Wind Speed'][(DataDF['Wind Speed']<0)|(DataDF['Wind Speed']>10)]=np.nan
    
    ReplacedValuesDF.loc['2. Gross Error',:]=DataDF.isnull().sum()-ReplacedValuesDF.loc['1. No Data']
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    # swap the values for Max and Min by finding if Man<Min
    count = 0
    value = 0
    
    for i in range(len(DataDF)):
        if DataDF['Max Temp'][i]<DataDF['Min Temp'][i]: #constrain
            value=DataDF['Max Temp'][i] # store data for later use
            DataDF['Max Temp'][i]=DataDF['Min Temp'][i]
            DataDF['Min Temp'][i]=value
            count += 1
    
    ReplacedValuesDF.loc['3. Swapped',:]=[0,count,count,0]
            
    return( DataDF, ReplacedValuesDF )    

    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    # find if Max-Min >25, replace value by nan
    count=0
    for i in range(len(DataDF)):
        if DataDF['Max Temp'][i]-DataDF['Min Temp'][i]>25: #constrain
            DataDF['Max Temp'][i]=np.nan
            DataDF['Min Temp'][i]=np.nan
            count += 1
  
    ReplacedValuesDF.loc['4. Range Fail',:]=[0,count,count,0
                        ]
    return( DataDF, ReplacedValuesDF )

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)



## plot for Metdata
import matplotlib.pyplot as plt

# precip data
Original=ReadData(fileName)[0]

Checked=DataDF

Original['Precip'].plot(color='red')
Checked['Precip'].plot(color='blue')
plt.xlabel('Date')
plt.ylabel('Precip')
plt.legend(['Original','Checked'])

plt.savefig('Precip plot.png')
plt.close()

# Max Temp Plot
Original['Max Temp'].plot(color='red')
Checked['Max Temp'].plot(color='blue')
plt.xlabel('Date')
plt.ylabel('Max Temp')
plt.legend(['Original','Checked'])

plt.savefig('Maximum Temperature.png')
plt.close()


# Min Temp Plot
Original['Min Temp'].plot(color='red')
Checked['Min Temp'].plot(color='blue')
plt.xlabel('Date')
plt.ylabel('Min Temp')
plt.legend(['Original','Checked'])

plt.savefig('Minimum Temperature.png')
plt.close()

# Wind Speed Plot
Original['Wind Speed'].plot(color='red')
Checked['Wind Speed'].plot(color='blue')
plt.xlabel('Date')
plt.ylabel('Wind Speed')
plt.legend(['Original','Checked'])


plt.savefig('Wind Speed.png')
plt.close()

















