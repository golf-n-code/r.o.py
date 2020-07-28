# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:45:24 2020

@author: Group 1 - Angela Beck, Johannes Knoerr, Lishan Qian, Devin Ulam
"""
import numpy as np
import pandas as pd
import datetime as dt #for time filtering
import requests #for API

#which city has which state and county codes (Used across different functions)
codeDict = { 
        'New York City':{'stateClean':'NY', 'state': '36', 'county':'061,047,005,085,081'},
        'Pittsburgh':{'stateClean':'PA', 'state': '42', 'county':'003'},
        'San Francisco':{'stateClean':'CA', 'state': '06', 'county':'075'},
        'Wausau':{'stateClean':'WI', 'state': '55', 'county':'073'},
        'Charleston':{'stateClean':'SC', 'state': '45', 'county':'019'}
}

def priceSF():
    #Read in raw data into df
    rawDF = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="zillow_valueSF_RAW")
    
    #drop out the columns that are outside of 2014-2017 timeframe
    for col in rawDF.columns:
        rawDF.columns.get_loc(col)
        try:
            date = dt.datetime.strptime(col,"%Y-%m")
            if date > dt.datetime.strptime('2017-12',"%Y-%m") or date < dt.datetime.strptime('2014-01',"%Y-%m"):
                rawDF = rawDF.drop(col, axis = 1)
        except:
            #do nothing for now
            next
    #drop the unnecessary columns
    rawDF = rawDF.drop(["Metro","SizeRank"], axis = 1)
    
    #build list of list of county and state
    countyList = [];
    for codes in codeDict.values():
        state = codes['state']
        county = codes['county']
        if len(county.split(',')) > 0:
            for code in county.split(","):
                countyList.append([int(state),int(code)])
        else:
            countyList.append([int(state),int(code)])
    countyList = [tuple(i) for i in countyList]
    
    #drop counties/state that are not of interest
    cleanDF = rawDF[rawDF[['StateCodeFIPS', 'MunicipalCodeFIPS']].apply(tuple, axis = 1).isin(countyList)]
    
    # remove some of the unwanted columns
    cleanDF.drop(['RegionID','StateCodeFIPS','MunicipalCodeFIPS','RegionName'], axis = 1, inplace = True)
    timeList = [col for col in cleanDF.columns if col not in ['State']]
    
    #transpose the years to be one column
    cleanDF = cleanDF.melt(id_vars=['State'], value_vars=timeList)
    cleanDF.columns = ['state','year','price']
    
    #clean year column
    cleanDF["year"] = cleanDF.apply(lambda row: row["year"].split("-")[0], axis = 1)
    
    #group by year and state
    cleanDF = cleanDF.groupby(['year','state'],as_index=False)['price'].mean()
    
    #convert data to ints
    for col in cleanDF.columns:
        if col not in ["state"]:
            cleanDF[col] = pd.to_numeric(cleanDF[col])
            
    return cleanDF
#------------------------- END ZILLOW SINGLE FAMILY PRICE CLEANING ---------------------------------------
  
#------------------------- START ZILLOW RENT INDEX CLEANING ----------------------------------------------
def rentIndex():
    #Read in raw data into df
    rawDF = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="zillow_rentIndex_RAW")
    
    #drop out the columns that are outside of 2014-2017 timeframe
    for col in rawDF.columns:
        rawDF.columns.get_loc(col)
        try:
            date = dt.datetime.strptime(col,"%Y-%m")
            if date > dt.datetime.strptime('2017-12',"%Y-%m") or date < dt.datetime.strptime('2014-01',"%Y-%m"):
                rawDF = rawDF.drop(col, axis = 1)
        except:
            #do nothing for now
            next
    #drop the unnecessary columns
    rawDF = rawDF.drop(["Metro","SizeRank"], axis = 1)
    
    #build list of list of county and state
    countyList = [];
    for codes in codeDict.values():
        state = codes['state']
        county = codes['county']
        if len(county.split(',')) > 0:
            for code in county.split(","):
                countyList.append([int(state),int(code)])
        else:
            countyList.append([int(state),int(code)])
    countyList = [tuple(i) for i in countyList]
    
    #drop counties/state that are not of interest
    cleanDF = rawDF[rawDF[['StateCodeFIPS', 'MunicipalCodeFIPS']].apply(tuple, axis = 1).isin(countyList)]
    
    # remove some of the unwanted columns
    cleanDF.drop(['RegionID','StateCodeFIPS','MunicipalCodeFIPS','RegionName'], axis = 1, inplace = True)
    timeList = [col for col in cleanDF.columns if col not in ['State']]
    
    #transpose the years to be one column
    cleanDF = cleanDF.melt(id_vars=['State'], value_vars=timeList)
    cleanDF.columns = ['state','year','rent']
    
    #clean year column
    cleanDF["year"] = cleanDF.apply(lambda row: row["year"].split("-")[0], axis = 1)
    
    #group by year and state
    cleanDF = cleanDF.groupby(['year','state'],as_index=False)['rent'].mean()
    
    #convert data to ints
    for col in cleanDF.columns:
        if col not in ["state"]:
            cleanDF[col] = pd.to_numeric(cleanDF[col])
            
    return cleanDF
#------------------------- END ZILLOW RENT INDEX CLEANING -------------------------------------

#------------------------- START ZILLOW RENT INDEX PER SQ FT CLEANING ----------------------------------------------
def rentIndexPerSqFt():
    #Read in raw data into df
    rawDF = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="zillow_rentIndexPerSqFt_RAW")
    
    #drop out the columns that are outside of 2014-2017 timeframe
    for col in rawDF.columns:
        rawDF.columns.get_loc(col)
        try:
            date = dt.datetime.strptime(col,"%Y-%m")
            if date > dt.datetime.strptime('2017-12',"%Y-%m") or date < dt.datetime.strptime('2014-01',"%Y-%m"):
                rawDF = rawDF.drop(col, axis = 1)
        except:
            #do nothing for now
            next
    #drop the unnecessary columns
    rawDF = rawDF.drop(["Metro","SizeRank"], axis = 1)
    
    #build list of list of county and state
    countyList = [];
    for codes in codeDict.values():
        state = codes['state']
        county = codes['county']
        if len(county.split(',')) > 0:
            for code in county.split(","):
                countyList.append([int(state),int(code)])
        else:
            countyList.append([int(state),int(code)])
    countyList = [tuple(i) for i in countyList]
    
    #drop counties/state that are not of interest
    cleanDF = rawDF[rawDF[['StateCodeFIPS', 'MunicipalCodeFIPS']].apply(tuple, axis = 1).isin(countyList)]
    
    # remove some of the unwanted columns
    cleanDF.drop(['RegionID','StateCodeFIPS','MunicipalCodeFIPS','RegionName'], axis = 1, inplace = True)
    timeList = [col for col in cleanDF.columns if col not in ['State']]
    
    #transpose the years to be one column
    cleanDF = cleanDF.melt(id_vars=['State'], value_vars=timeList)
    cleanDF.columns = ['state','year','rentpersqft']
    
    #clean year column
    cleanDF["year"] = cleanDF.apply(lambda row: row["year"].split("-")[0], axis = 1)
    
    #group by year and state
    cleanDF = cleanDF.groupby(['year','state'],as_index=False)['rentpersqft'].mean()
    
    #convert data to ints
    for col in cleanDF.columns:
        if col not in ["state"]:
            cleanDF[col] = pd.to_numeric(cleanDF[col])
            
    return cleanDF
#------------------------- END ZILLOW RENT INDEX PER SQ FT CLEANING -------------------------------------
    
#------------------------- BEGIN BUSINESS ESTABLISHMENT API CLEANING -------------------------------------
def startupAPI(): #read in data from API for each year

    #reset master dataframe
    try:
        id(masterDF)
        masterDF = masterDF.empty #empty if exists
    except:
        pass
    for city,codes in codeDict.items():
        print(city)
        stateCode = codes["state"]
        countyCode = codes["county"]
        for i in range(2014,2018):
            res = requests.get("https://api.census.gov/data/" + str(i) + "/cbp?get=YEAR,ESTAB,EMP,EMPSZES&for=county:" + countyCode + "&in=state:" + stateCode) #get data from API
            data = res.json()
            headers = data[0] #headers are first in list
            df = pd.DataFrame(data[1:], columns=headers)
            try: #if masterDF exists, then append it
                id(masterDF)
                masterDF = pd.concat([df,masterDF])
            except:
                masterDF = df
                
    #convert data to ints
    for col in masterDF.columns:
        if col not in ["state","county"]:
            masterDF[col] = pd.to_numeric(masterDF[col])
    
    #aggregate by state to account for NYC having multiple counites
    grpByCounty = masterDF.groupby(['YEAR','state'],as_index=False)['ESTAB','EMP','EMPSZES'].sum()
    
    #add city and state columns
    grpByCounty["City"] = grpByCounty.apply(lambda row: getCity(row["state"]), axis = 1)
    grpByCounty["StateClean"] = grpByCounty.apply(lambda row: getStateClean(row["state"]), axis = 1)
    
    #drop state code
    grpByCounty.drop(['state'], axis = 1, inplace = True)
    grpByCounty = grpByCounty.rename({'StateClean':'State'}, axis=1)
    grpByCounty.columns = map(str.lower, grpByCounty.columns)
    return grpByCounty

#------------------ START EXTRACTING POPULATION BY SEX AND RACE PER COUNTY DATA ------------------
# screen scrape demographic information from data.gov
def loadPopulationBySexAndRaceData():
    
    # read in data
    df = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="populationBySexAndRace_RAW")

    # rename columns
    df.columns = ['year_id', 'date', 'sex_id', 'sex',
       'hisp_id', 'hispanic_status', 'geo_id', 'geo_zip',
       'county_state', 'total_pop', 'white', 'black', 'american_indian', 'asian', 'hawaiian', 'two_or_more_races']

    # delete first row
    df = df.drop(df.index[0])

    # split data
    df[['county','state']] = df['county_state'].str.split(",",expand=True,)
    df['year'] = df['year_id'].str[-4:]
   
    df = df[df.hispanic_status == 'Total']
   
    # remove some of the unwanted columns
    df.drop(['year_id','date','sex_id','hisp_id','geo_id','county_state','hispanic_status', 'geo_zip'], axis = 1, inplace = True)
   
    # isolate date range of interest: 2014 - 2017
    df = df[(df.year == '2014') | (df.year == '2015') | (df.year == '2016') | (df.year == '2017')]
   
    # remove extra spaces from state column entries
    df.state = df.state.str.strip()
   
     # replace full state names with abbreviations
    for i in df.index:
        df.at[i, 'state'] = 'NY' if df.at[i, 'state'] == 'New York' else df.at[i, 'state']
        df.at[i, 'state'] = 'PA' if df.at[i, 'state'] == 'Pennsylvania' else df.at[i, 'state']
        df.at[i, 'state'] = 'CA' if df.at[i, 'state'] == 'California' else df.at[i, 'state']
        df.at[i, 'state'] = 'WI' if df.at[i, 'state'] == 'Wisconsin' else df.at[i, 'state']
        df.at[i, 'state'] = 'SC' if df.at[i, 'state'] == 'South Carolina' else df.at[i, 'state']  
   
    # isolate counties of interest
    df = df[((df.county == 'New York County') & (df.state == 'NY')) |
            ((df.county == 'Kings County') & (df.state == 'NY')) |
            ((df.county == 'Bronx County') & (df.state == 'NY')) |
            ((df.county == 'Richmond County') & (df.state == 'NY')) |
            ((df.county == 'Queens County') & (df.state == 'NY')) |
            ((df.county == 'Allegheny County') & (df.state == 'PA')) |
            ((df.county == 'San Francisco County') & (df.state == 'CA')) |
            ((df.county == 'Marathon County') & (df.state == 'WI')) |
            ((df.county == 'Charleston County') & (df.state == 'SC'))]
   
    # cast numeric fields
    df[['total_pop','white','black','american_indian','asian','hawaiian','two_or_more_races']] = df[['total_pop','white','black','american_indian','asian','hawaiian','two_or_more_races']].apply(pd.to_numeric)
   
    # use group by to combine NY counties
    df = df.groupby(['year','state','sex'], as_index=False)[['total_pop','white','black','american_indian','asian','hawaiian','two_or_more_races']].mean()

    # separate data based on sex
    df_both = df[df.sex == 'Both Sexes']
    df_male = df[df.sex == 'Male']
    df_female = df[df.sex == 'Female']    
   
    # merge the separated data sets
    df_merged = pd.merge(df_both, df_male, how='left', on=['year','state'])
    df = pd.merge(df_merged, df_female, how='left', on=['year','state'])
   
    # drop columns that are no longer needed
    df.drop(['sex_x','sex_y','sex'], axis = 1, inplace = True)
   
    # rename columns to correctly identify sex
    df.columns = ['year', 'state', 'total_pop_both', 'white_both', 'black_both',
       'american_indian_both', 'asian_both', 'hawaiian_both', 'two_or_more_races_both',
       'total_pop_male', 'white_male', 'black_male', 'american_indian_male', 'asian_male',
       'hawaiian_male', 'two_or_more_races_male', 'total_pop_female', 'white_female', 'black_female',
       'american_indian_female', 'asian_female', 'hawaiian_female', 'two_or_more_races_female']
    df["state"] = df["state"].apply(str)
    df["year"] = df["year"].apply(int)
    return df

#------------------ END EXTRACTING POPULATION BY SEX AND RACE PER COUNTY DATA ------------------


#------------------ START EXTRACTING POVERTY PER COUNTY DATA ------------------
def loadPovertyData():
    # screen scrape demographic information from data.gov
    
    # read in data
    df = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="povertyDataByCounty_RAW")
    
    # split location data
    df[['county','state']] = df['Name'].str.split(",",expand=True,)
    
    # clean all df values by removing excess spaces
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # remove some of the unwanted columns
    df.drop(['State FIPS code','County FIPS code','Name',2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1995,1993,1989], axis = 1, inplace = True)
        
    # fill all 'None' fields in state column
    df['state'].fillna('--',inplace = True)
        
    # assign missing state values
    for i in df.index:
        df.at[i, 'state'] = df.at[i, 'county'] if df.at[i, 'state'] == '--' else df.at[i, 'state']
            
    # replace full state names with abbreviations
    for i in df.index:
        df.at[i, 'state'] = 'NY' if df.at[i, 'state'] == 'New York' else df.at[i, 'state']
        df.at[i, 'state'] = 'PA' if df.at[i, 'state'] == 'Pennsylvania' else df.at[i, 'state']
        df.at[i, 'state'] = 'CA' if df.at[i, 'state'] == 'California' else df.at[i, 'state']
        df.at[i, 'state'] = 'WI' if df.at[i, 'state'] == 'Wisconsin' else df.at[i, 'state']
        df.at[i, 'state'] = 'SC' if df.at[i, 'state'] == 'South Carolina' else df.at[i, 'state']
      
    # isolate REGIONS of interest: NY, PA, CA, WI, SC
    df = df[((df.county == 'New York County') & (df.state == 'NY')) | 
            ((df.county == 'Kings County') & (df.state == 'NY')) | 
            ((df.county == 'Bronx County') & (df.state == 'NY')) | 
            ((df.county == 'Richmond County') & (df.state == 'NY')) | 
            ((df.county == 'Queens County') & (df.state == 'NY')) | 
            ((df.county == 'Allegheny County') & (df.state == 'PA')) | 
            ((df.county == 'San Francisco County') & (df.state == 'CA')) | 
            ((df.county == 'Marathon County') & (df.state == 'WI')) | 
            ((df.county == 'Charleston County') & (df.state == 'SC'))]
    
    df = df.groupby('state', as_index=False).mean()
    
    df = df.melt(id_vars=['state'], value_vars=[2017,2016,2015,2014])
    
    df.columns = ['state','year','poverty']
    df['year'] = df['year'].map(lambda x: int(x))
    return df

#------------------ END EXTRACTING POVERTY PER COUNTY DATA ------------------
    
#--------------------- BEGIN EXTRACTING UNEMPLOYMENT DATA --------------------------------
def loadUnemploymentData():

    # read in data
    df_NY = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="newYorkUnemployment_RAW")
    df_PA = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="pennsylvaniaUnemployment_RAW")
    df_CA = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="californiaUnemployment_RAW")
    df_WI = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="wisconsinUnemployment_RAW")
    df_SC = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="southCarolinaUnemployment_RAW")

    df = pd.concat([df_NY, df_PA, df_CA, df_WI, df_SC])

    # split location data
    df[['county','state']] = df['Name'].str.split(",",expand=True,)
    
    # clean all df values by removing excess spaces
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # drop all columns with "None" in the county field
    df = df.dropna()
    
    # remove some of the unwanted columns
    df.drop(['FIPS','Name',2010,2011,2012,2013,2018], axis = 1, inplace = True)
    
    # isolate REGIONS of interest: NY, PA, CA, WI, SC
    df = df[((df.county == 'New York County') & (df.state == 'NY')) | 
            ((df.county == 'Kings County') & (df.state == 'NY')) | 
            ((df.county == 'Bronx County') & (df.state == 'NY')) | 
            ((df.county == 'Richmond County') & (df.state == 'NY')) | 
            ((df.county == 'Queens County') & (df.state == 'NY')) | 
            ((df.county == 'Allegheny County') & (df.state == 'PA')) | 
            ((df.county == 'San Francisco County/city') & (df.state == 'CA')) | 
            ((df.county == 'Marathon County') & (df.state == 'WI')) | 
            ((df.county == 'Charleston County') & (df.state == 'SC'))]
     
    # use group by to combine NY counties
    df = df.groupby('state', as_index=False).mean()
    
    df = df.melt(id_vars=['state','Median Household Income (2018)','% of State Median HH Income'], value_vars=[2017,2016,2015,2014])

    df.columns = ['state','median_household_income','perc_of_state_median_household_income','year','unemployment_rate']

    return df

#--------------------- END EXTRACTING UNEMPLOYMENT DATA --------------------------------
    
#--------------------- BEGIN EXTRACTING AIRBNB DATA --------------------------------
def processAirbnb(df, name):
    #Export raw data
    df.to_excel('airbnbScrapeData/' + name + '_raw.xlsx')
    
    #Drop non-required columns
    df = df.drop(['accuracy', 'bathType', 'bedType', 'bedroomType', 'checkin', \
                            'cleanliness', 'communication', 'location', 'numHostReviews', \
                            'responseTimeShown', 'roomID', 'roomType', 'value'], axis = 1)
    #Count NaNs per column
    #for col in df.columns:
        #print('NaNs in ', col, ': ', df[col].isna().sum())

    #Delete columns with too many NaNs
    df = df.drop(['guestSatisfaction', 'numReviews', 'rating'], axis = 1)
    
    #Add city name column
    df['City'] = name
    
    #Reset index
    df = df.reset_index(drop = True)
    
    #Export cleaned data
    df.to_excel('airbnbScrapeData/' + name + '_cleaned.xlsx')
    
    return df
#--------------------- END EXTRACTING AIRBNB DATA --------------------------------
    
#------------------------Miscellaneous functions-------------------------------
def getCity(state): #define a function that we will use to translate state code to city name
    for city, codes in codeDict.items():
        if codes["state"] == state:
            return city
        else:
            continue
    return "N/A"
def getStateClean(state): #define a function that we will use to translate state code to state name
    for city, codes in codeDict.items():
        if codes["state"] == state:
            return codes["stateClean"]
        else:
            continue
    return "N/A"