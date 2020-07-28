# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:04:58 2020

@author: Group 1 - Angela Beck, Johannes Knoerr, Lishan Qian, Devin Ulam

Inspirations:
    https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
    https://machinelearningmastery.com/time-series-forecasting-methods-in-python-cheat-sheet/
    https://www.analyticsvidhya.com/blog/2018/09/multivariate-time-series-guide-forecasting-modeling-python-codes/
    
"""

import numpy as np
import pandas as pd
import datetime as dt #for time filtering
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import math
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
import datetime as dt

pd.set_option('display.max_columns', 25)
pd.set_option('display.max_rows', 50)

##################################
######## DATA PREP ###############
##################################
def getEntireSeries():
    #which city has which state and county codes (Used across different functions)
    codeDict = { 
            'New York City':{'stateClean':'NY', 'state': '36', 'county':'061,047,005,085,081'},
            'Pittsburgh':{'stateClean':'PA', 'state': '42', 'county':'003'},
            'San Francisco':{'stateClean':'CA', 'state': '06', 'county':'075'},
            'Wausau':{'stateClean':'WI', 'state': '55', 'county':'073'},
            'Charleston':{'stateClean':'SC', 'state': '45', 'county':'019'}
    }
    
    #Read in raw data into df
    rawDF = pd.read_excel('./CompiledData/DataFocusedPython_Group1_RAW.xlsx', sheet_name="zillow_valueSF_RAW")
    
    #drop the unnecessary columns
    rawDF = rawDF.drop(["Metro","SizeRank"], axis = 1)
    
    if True: #Reduce prediction on our counties
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
    else:
        cleanDF = rawDF
    
    # remove some of the unwanted columns
    cleanDF.drop(['RegionID','StateCodeFIPS','MunicipalCodeFIPS','RegionName'], axis = 1, inplace = True)
    timeList = [col for col in cleanDF.columns if col not in ['State']]
    
    #convert data to ints
    for col in cleanDF.columns:
        if col not in ["State"]:
            cleanDF[col] = pd.to_numeric(cleanDF[col])
      
    #cleanDF.to_csv("temp.csv", index = False) 
    return cleanDF
    

##################################
#### TIME SERIES FORECAST ########
##################################

cleanDF = getEntireSeries()
#cleanDF = pd.read_csv("temp.csv")

cleanDF = cleanDF.groupby('State').mean()
#cleanDF = cleanDF.transpose()
cleanDF = np.transpose(cleanDF)
cleanDF = cleanDF.reset_index()
cleanDF['index'] = cleanDF['index'].map(lambda x: pd.to_datetime(x, format='%Y-%m'))
cleanDF = cleanDF.set_index('index')

def performARIMA(series, p, d, q, plots = True):
    rcParams['figure.figsize'] = 18, 8
    
    series.dropna(inplace=True)
    if plots:
        series.plot()
        plt.title('Original data')
        plt.show()
    
    #Check stationarity with Dickey Fuller Test
    adtest = adfuller(series, autolag='AIC')
    if plots:
        print("Dickey Fuller p-value original data: ", adtest[1])
    
    #Examine dataframe: Try log and check moving average
    series_log = np.log(series)
    #series_log.plot()
    #plt.show()
    mavg = series_log.rolling(12).mean()
    #plt.plot(series_log)
    #plt.plot(mavg, color='red')   
    #plt.show()
    series_log_mavg = series_log - mavg
    #series_log_mavg.plot()
    #plt.show()
    series_log_mavg.dropna(inplace=True)
    adtest = adfuller(series_log_mavg, autolag='AIC')
    #print("p-value: ", adtest[1])
    
    #Try Differencing
    series_log_diff = series_log - series_log.shift()
    series_log_diff.dropna(inplace=True)
    #series_log_diff.plot()
    #plt.show()
    adtest = adfuller(series_log_mavg, autolag='AIC')
    if plots:
        print("Dickey Fuller p-value logarithmic and first difference: ", adtest[1]) #Better stationarity
    decomposition = seasonal_decompose(series_log)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    series_resid = residual
    series_resid.dropna(inplace=True)
    adtest = adfuller(series_resid, autolag='AIC')
    if plots:
        print("Dickey Fuller p-value residual after decomposition: ", adtest[1]) #Better stationarity
    
    
    #Hence use differencing --> ARIMA model
    #Check autocorrelations and partial autocorrelations for ARIMA
    lag_acf = acf(series_log_diff, nlags=20) #For p
    lag_pacf = pacf(series_log_diff, nlags=20, method='ols') #For q
    
    if plots:
        plt.plot(lag_acf)
        plt.axhline(y=0,linestyle='--',color='gray')
        plt.axhline(y=-1.96/np.sqrt(len(series_log_diff)),linestyle='--',color='gray')
        plt.axhline(y=1.96/np.sqrt(len(series_log_diff)),linestyle='--',color='gray')
        plt.title('Autocorrelation Function')
        plt.show()
    
        plt.plot(lag_pacf)
        plt.axhline(y=0,linestyle='--',color='gray')
        plt.axhline(y=-1.96/np.sqrt(len(series_log_diff)),linestyle='--',color='gray')
        plt.axhline(y=1.96/np.sqrt(len(series_log_diff)),linestyle='--',color='gray')
        plt.title('Partial Autocorrelation Function')
        plt.show()
    
    #Choose ARIMA(15,1,1)
    train = series_log[:math.floor(0.8*len(series_log))]
    test = series_log[math.floor(0.8*len(series_log))+1:]
    model = ARIMA(train, order=(p,d,q))
    model_fit = model.fit(disp=-1)
    if plots:
        plt.plot(series_log_diff[:math.floor(0.8*len(series_log))])
        plt.plot(model_fit.fittedvalues[:math.floor(0.8*len(series_log))], color='red')
        plt.title('ARIMA Training')
        plt.show()
    
    #Testing
    pred = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    #pred = model_fit.predict(start=train.index[-1], end=test.index[len(test.index)-1], dynamic=False)
    error = mean_squared_error(test, pred)
    if plots:
        print('Test MSE: %.3f' % error)
        plt.plot(series_log_diff[math.floor(0.8*len(series_log))+1:])
        plt.plot(pred, color='red')
        plt.title('ARIMA Testing')
        plt.show()
    
    #Back to original values
    training_ARIMA_diff = pd.Series(model_fit.fittedvalues, copy=True)
    testing_ARIMA_diff = pd.Series(pred, copy=True)
    model_diff_cum_sum = training_ARIMA_diff.append(testing_ARIMA_diff)
    model_diff_cum_sum = model_diff_cum_sum.cumsum()
    modelResults_log = pd.Series(series_log.ix[0], index=series_log.index) 
    modelResults_log = modelResults_log.add(model_diff_cum_sum,fill_value=0)
    modelResults = np.exp(modelResults_log[:-1])
    
    if plots:
        plt.plot(series)
        plt.plot(modelResults)
        plt.axvline(x=series.index[math.floor(0.8*len(series_log))], color='red')
        plt.title('Fit original data')
        plt.show()   
    
    #Out-of-sample-forecast
    forecast_range = 12
    
    train = series_log #Train now on entire dataframe
    model = ARIMA(train, order=(p,d,q))
    model_fit = model.fit(disp=-1)   
    pred = model_fit.predict(start=len(train), end=len(train)+forecast_range, dynamic=False) #Do real out-of-sample forecasts
    training_ARIMA_diff = pd.Series(model_fit.fittedvalues, copy=True)
    testing_ARIMA_diff = pd.Series(pred, copy=True)
    model_diff_cum_sum = training_ARIMA_diff.append(testing_ARIMA_diff)
    model_diff_cum_sum = model_diff_cum_sum.cumsum()
    modelResults_log = pd.Series(series_log.ix[0], index=series_log.index.union([pd.to_datetime('2020-'+str(i), format='%Y-%m') for i in range(1,13)]))#+[pd.to_datetime('2021-'+str(i), format='%Y-%m') for i in range(1,13)])) 
    modelResults_log = modelResults_log.add(model_diff_cum_sum,fill_value=0)
    modelResults = np.exp(modelResults_log[:-1])
    oos = modelResults[-(forecast_range):]
    
    series = series.append(round(oos,2))
    
    #Return out-of-sample forecast
    return round(series,2)


#Univariate process for each standalone county   
#San Francisco
print('\nSan Francisco')
series = cleanDF[cleanDF.columns[0]]
forecast_SF = performARIMA(series,15,1,1, plots = False) 

#New York
print('\nNew York')
series = cleanDF[cleanDF.columns[1]]
forecast_NY = performARIMA(series,20,1,1, plots = False) 

#Pittsburgh
print('\nPittsburgh')
series = cleanDF[cleanDF.columns[2]]
forecast_PI = performARIMA(series,3,1,2, plots = False) 

#Charleston
print('\nCharleston')
series = cleanDF[cleanDF.columns[3]]
forecast_CH = performARIMA(series,0,1,2, plots = False) 

#Wausau
print('\nWausau')
series = cleanDF[cleanDF.columns[4]]
forecast_WA = performARIMA(series,10,1,2, plots = False) 

#Merge data together
fullData = pd.DataFrame({'San Francisco': forecast_SF, 'New York City': forecast_NY, 'Pittsburgh': forecast_PI, 'Charleston': forecast_CH, 'Wausau': forecast_WA})

#Write to csv
fullData.to_csv('./CompiledData/forecastData.csv')




