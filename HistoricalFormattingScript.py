# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 10:27:07 2021

@author: Ben McCarthy
"""
#INPUTS
FileIn =r'Historical Data'


import os
import pandas as pd


#set the working directory
os.chdir(FileIn)

files = os.listdir(FileIn)

files_xls = [f for f in files if f[-3:] == 'xls']
files_xls

#start with blank dataframe
df = pd.DataFrame()

#parse through xls files in directory, append them all together into new dataframe
for f in files_xls:
    data = pd.read_excel(f)
    df = df.append(data)


df['Collection_Date&Time'] = pd.to_datetime(df['Collection_Date&Time'] )
 
droplist = ['List of results to drop' ]   
   
    
df = df[~df.Sample_Description.isin(droplist)]  


MSlist = ['Matrix Spike Matrix Spike Duplicate lists']   
dfMS = df.copy()

dfMS = dfMS[dfMS.Sample_Description.isin(MSlist)]


DUPlist = ['Lab duplicate list']
dfDUP = df.copy()

dfDUP = dfDUP[dfDUP.Sample_Description.isin(DUPlist)]

droplist = ['Duplicates to drop']

df = df[~df.Sample_Description.isin(droplist)]

#we're going to write out a function that can process out data for the Historical, DUPEs, and MS/MSD data
def EGLE_Format(df):
    #for the sake of comPatibility in functions, we will change around some column dtypes 
    df['Result'] = df['Result'].astype(str)
    df['RL'] = df['RL'].astype(str)
    df['Qualifier'] = df['Qualifier'].astype(str)

    #We want any df['Result'] cell that has ND to be changed to the RL value with a "<" symbol before that. 
    df['Result'] = df.apply(lambda x: str('<')+x['RL'] if x['Result'] == "ND" else x['Result'], axis=1)

    #now we need to include any qualifiers that may have been present in there as well
    df['Result'] = df.apply(lambda x: x['Result']+str(' ')+x['Qualifier'] if x['Qualifier'] == 'T'
                        or x['Qualifier'] == 'X' or x['Qualifier'] == 'X1' else x['Result'], axis=1)

    #Our last step is to pivot the whole table, we need the analytes as the indexes and the wells/dates on the columns
    test = df.pivot_table(index='Analyte',columns=['Sample_Description','Collection_Date&Time'],values=['Result'],aggfunc ='first')

    #lets try to sort the wells so that similar names are together alphabetically
    test = test.sort_index(level=[0,1],axis=1,ascending=[True,True])
    
    return test

#run the function for each of our desired datasets
dfHistorical = EGLE_Format(df)

dfDUPES = EGLE_Format(dfDUP)

dfMSDs = EGLE_Format(dfMS)

#write out our dataframes to csv files, then we can open them in excel and make them look right
dfHistorical.to_csv(r'Savename.csv')

dfDUPES.to_csv(r'savename.csv')

dfMSDs.to_csv(r'savename.csv')

