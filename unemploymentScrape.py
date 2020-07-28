# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:12:15 2020

@author: Group 1 - Angela Beck, Johannes Knoerr, Lishan Qian, Devin Ulam

Inspirations from http://toddhayton.com/2015/05/14/using-selenium-to-scrape-aspnet-pages-with-ajax-pagination/
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
    

####################################
######### A: Scraping ##############
####################################
def scrapeUnemployment():
    #Dataframe to be filled
    df = pd.DataFrame(columns = ['FIPS', 'Name', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', 'Median Income 2018', '% of State Median Household Income', 'State'])
    
    #Special case: Alabama
    url = "https://data.ers.usda.gov/reports.aspx?ID=17828"
    
    #Create driver
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)   
    driver.switch_to.default_content()
    
    #Select respective state
    xpath = '/html/body/form/div[7]/div/div/div/div[2]/div/table/tbody/tr[2]/td/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[4]/td[3]/div/a'
    state_name = driver.find_element_by_xpath(xpath).get_attribute('innerHTML')   
    driver.find_element_by_xpath(xpath).click()        
    driver.implicitly_wait(10)     
    
    #Grab data table and copy to Dataframe
    table = driver.find_element_by_xpath('/html/body/form/div[7]/div/div/div/div[2]/div/table/tbody/tr[2]/td/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table')
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows[17:]:
        listItems = row.text.split('\n')
        df.loc[len(df)] = listItems + [state_name]
    pd.set_option('display.max_columns', 25)       
    
    #Close driver
    driver.quit()
    
    #Other states
    state_range = range(5,55) #Note: this does not include Alabama
    for i in state_range:    
        url = "https://data.ers.usda.gov/reports.aspx?ID=17828"
        
        #Create driver
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)    
        driver.switch_to.default_content()
        
        #Select respective state
        xpath = '/html/body/form/div[7]/div/div/div/div[2]/div/table/tbody/tr[2]/td/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[' + str(i) + ']/td[3]/div/a'    
        state_name = driver.find_element_by_xpath(xpath).get_attribute('innerHTML')
        driver.find_element_by_xpath(xpath).click()          
        driver.implicitly_wait(10)      
        
        #Grab data table and copy to Dataframe
        table = driver.find_element_by_xpath('/html/body/form/div[7]/div/div/div/div[2]/div/table/tbody/tr[2]/td/div/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table')
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows[17:]:
            listItems = row.text.split('\n')
            df.loc[len(df)] = listItems + [state_name]
        pd.set_option('display.max_columns', 25)
            
        #Close driver
        driver.quit()
        
    return df


def goScrape():      
    #Perform scraping  
    if True:
        unemploymentData = scrapeUnemployment()
        unemploymentData.to_csv('unemployment_Raw.csv', index = False)
        unemploymentData.to_excel('unemployment_Raw.xlsx')
       
    ####################################
    ####### B: Data Cleaning ###########
    ####################################
    
    #Read from checkpoint
    unemploymentData = pd.read_csv('unemployment_Raw.csv')
    
    #Rearrange columns
    unemploymentData = unemploymentData[unemploymentData.columns.tolist()[0:2] + unemploymentData.columns.tolist()[-1:] + unemploymentData.columns.tolist()[3:len(unemploymentData.columns.tolist())-1]]
    
    #Export
    unemploymentData.to_excel('unemployment_Clean.xlsx')
    
    ####################################
    ###### C: Data Preparation #########
    ####################################
    aggregateData = pd.DataFrame(columns = ['Year', 'State', 'City', 'Unemployment'])
    
    #Pittsburgh
    pittData = unemploymentData[unemploymentData['Name'].str.contains('Allegheny')]
    for i in range(6,10):
        aggregateData.loc[len(aggregateData)] = [pittData.columns.tolist()[i], 'PA', 'Pittsburgh', pittData.iloc[0,i]]
    
    #New York
    #Note: Simple Average --> does not take into account different population sizes in different counties!
    nyData = unemploymentData[unemploymentData['Name'].str.contains('Bronx') | \
                              unemploymentData['Name'].str.contains('New York') |
                              unemploymentData['Name'].str.contains('Queens') |
                              unemploymentData['Name'].str.contains('Kings County, NY') |
                              unemploymentData['Name'].str.contains('Richmond County, NY')
                              ]
    for i in range(6,10):
        aggregateData.loc[len(aggregateData)] = [nyData.columns.tolist()[i], 'NY', 'New York City', round(nyData.iloc[:,i].mean(),2)]
     
    #San Francisco
    sfData = unemploymentData[unemploymentData['Name'].str.contains('San Francisco')]
    for i in range(6,10):
        aggregateData.loc[len(aggregateData)] = [sfData.columns.tolist()[i], 'CA', 'California', sfData.iloc[0,i]]
    
    #Wausau
    wauData = unemploymentData[unemploymentData['Name'].str.contains('Marathon')]
    for i in range(6,10):
        aggregateData.loc[len(aggregateData)] = [wauData.columns.tolist()[i], 'WI', 'Wausau', wauData.iloc[0,i]]
    
    #Charleston
    #Note: Simple Average --> does not take into account different population sizes in different counties!
    chData = unemploymentData[unemploymentData['Name'].str.contains('Charleston County, SC') | \
                              unemploymentData['Name'].str.contains('Berkeley County, SC')
                              ]
    for i in range(6,10):
        aggregateData.loc[len(aggregateData)] = [chData.columns.tolist()[i], 'SC', 'Charleston', round(chData.iloc[:,i].mean(),2)]
    
    
    pd.set_option('display.max_columns', 25)
    #print(aggregateData)
    
    #final cleaning to match merged data
    aggregateData.columns = ["year","state","city","unemployment"]
    aggregateData["state"] = aggregateData["state"].apply(str)
    aggregateData["year"] = aggregateData["year"].apply(int)
    
    return aggregateData
