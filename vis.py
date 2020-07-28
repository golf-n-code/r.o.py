# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:40:52 2020

@author: Group 1 - Angela Beck, Johannes Knoerr, Lishan Qian, Devin Ulam
"""
import clean as clean
import pandas as pd
import unemploymentScrape as scrape
import re
import matplotlib.pyplot as plt
import numpy as np
import pylab
from os import path

doDataCollection = False
if path.exists('mergedDF.csv'):
    i = 0
    #Ask if you would like to run the data extraction/cleaning script, or load the clean, merged dataframe from CSV
    while i == 0:
        rerun = input("\nWould you like to reload the data, or use the existing dataframe?\n1. Rerun\n2. Use existing data\n(Please type a 1 or a 2 and press enter)")
        try:
            if re.search(r'^[1-2]$', rerun) != None:
                    print("Thank you for your decision.")
                    if rerun == "1":
                        doDataCollection = True
                    i = 1
        except ValueError:
            print("This is not a valid number. Please make another selection by entering a 1 or a 2.")
else:
    doDataCollection = True

if doDataCollection:
    print("Data Extraction and Cleaning has begun...")
    #BUSINESS ESTABLISHMENT DATAFRAME
    startupDF = clean.startupAPI()
    #END BUSINESS ESTABLISHMENT
    
    #HOUSING DATAFRAMES
    SFpurchaseDF = clean.priceSF()
    rentIndexDF = clean.rentIndex()
    rentPerSqFtDF = clean.rentIndexPerSqFt()
    #END HOUSING
    
    #DEMOGRAPHIC DATAFRAMES
    povertyDF = clean.loadPovertyData()
    sexRaceDF = clean.loadPopulationBySexAndRaceData()
    #END DEMOGRAPHICS
    
    #UNEMPLOYMENT SCRAPING
    unemployDF = scrape.goScrape()
    #END UNEMPLOYMENT
    
    #merge dataframes
    mergedDF = []
    mergedDF = pd.merge(startupDF, SFpurchaseDF, how='left', on=["year","state"])
    mergedDF = pd.merge(mergedDF, rentIndexDF, how='left', on=["year","state"]) #continue merging
    mergedDF = pd.merge(mergedDF, rentPerSqFtDF, how='left', on=["year","state"]) #continue merging
    mergedDF = pd.merge(mergedDF, povertyDF, how='left', on=["year","state"]) #continue merging
    mergedDF = pd.merge(mergedDF, unemployDF, how='left', on=["year","state"]) #continue merging
    mergedDF = pd.merge(mergedDF, sexRaceDF, how='left', on=["year","state"]) #continue merging
    mergedDF.to_csv('mergedDF.csv', index = False)
    print("Data Extraction and Cleaning has finished...")
else:
    mergedDF = pd.read_csv('mergedDF.csv')

#START USER INPUT
i = 0
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#1. Ask for desired pricing model
while i == 0:
    input_priceModel = input("\nWhat pricing model would you like to utilize?\n1. Annual License\n2. Query Level\n(Please type a 1 or a 2 and press enter)")
    try:
        if re.search(r'^[1-2]$', input_priceModel) != None:
                print("Thank you for the pricing model selection.")
                i = 1
    except ValueError:
        print("This is not a valid number. Please make another selection by entering a 1 or a 2.")

end = 0
while end == 0:
    i = 0
    #2. Ask for region(s) of interest (only if query level pricing was chosen)
    if input_priceModel == '2': # only ask for regions of interest if query level pricing is chosen
        while i == 0:
            input_regions = input("\nWhat region(s) would you like to evaluate?\n1. New York City, NY\n2. Pittsburgh, PA\n3. San Francisco, CA\n4. Wausau, WI\n5. Charleston, SC\n(If you would like to analyze more than one city, please separate your input values with a comma and no spaces.)")
            try:
                if re.search(r'^[1-5]((,[1-5])?)*$', input_priceModel) != None:
                    print("Thank you for sharing your region(s) of interest.")
                    i = 1
            except ValueError:
                print("This is not a valid input.  Please enter values between 1 and 5, separated by commas.")
    else:
        input_regions = 0
    
    # map input_regions to cities
    regions_dict = { 
            0:'All',
            1:'New York City',
            2:'Pittsburgh',
            3:'San Francisco',
            4:'Wausau',
            5:'Charleston'}
    
    #3. Ask what data output is preferred
    i = 0
    while i == 0:
        input_dataType = input("\nHow would you like for your data to be displayed?\n1. Table\n2. Plot\n(Please type a 1 or a 2 and press enter.)")
        try:
            if re.search(r'^[1-2]$', input_dataType) != None:
                    print("Thank you for specifying your display of interest.")
                    i = 1
        except ValueError:
            print("This is not a valid number. Please make another selection by entering a 1 or a 2.")
    
    i = 0
    #4. Ask what variables are of interest
    if input_dataType == '1': # allow user to choose as many variables as desired for the table output
        while i == 0:
            input_variables = input("\nWhat demographic/socioeconomic variables would you like to evaluate?\n1. Number of business establishments.\n2. Number of employees.\n3. Employment size of establishments.\n4. Average housing price.\n5. Average rent price.\n6. Average rent per square foot.\n7. Number of citizens in poverty.\n8. Unemployment rate.\n9. Total population.\n10. Total White population.\n11. Total Black population.\n12. Total American Indian population.\n13. Total Asian population.\n14. Total Hawaiian population.\n15. Total population with one or more races.\n16. Total male population.\n17. Total White males.\n18. Total Black males.\n19. Total American Indian males.\n20. Total Asian males.\n21. Total Hawaiian males.\n22. Total males with one or more races.\n23. Total female population.\n24. Total White females.\n25. Total Black females.\n26. Total American Indian females.\n27. Total Asian females.\n28. Total Hawaiian females.\n29. Total females with one or more races.\n(Please separate your input values with a comma and no spaces.)")
            try:
                if re.search(r'^([1-9]|[12][0-9]|3[01])((,([1-9]|[12][0-9]|3[01]))?)*$', input_variables) != None:
                    print("Thank you for sharing your demographic/socioeconomic variables of interest.")
                    i = 1
            except ValueError:
                print("This is not a valid input.  Please enter values between 1 and 31, separated by commas.")
    else: # ask user to choose two variables to plot
        while i == 0:
            input_variables = input("\nWhat two demographic/socioeconomic variables would you like to plot?\n1. Number of business establishments.\n2. Number of employees.\n3. Employment size of establishments.\n4. Average housing price.\n5. Average rent price.\n6. Average rent per square foot.\n7. Number of citizens in poverty.\n8. Unemployment rate.\n9. Total population.\n10. Total White population.\n11. Total Black population.\n12. Total American Indian population.\n13. Total Asian population.\n14. Total Hawaiian population.\n15. Total population with one or more races.\n16. Total male population.\n17. Total White males.\n18. Total Black males.\n19. Total American Indian males.\n20. Total Asian males.\n21. Total Hawaiian males.\n22. Total males with one or more races.\n23. Total female population.\n24. Total White females.\n25. Total Black females.\n26. Total American Indian females.\n27. Total Asian females.\n28. Total Hawaiian females.\n29. Total females with one or more races.\n(Please separate your input values with a comma and no spaces.)")
            try:
                if re.search(r'^([1-9]|[12][0-9]|3[01]),([1-9]|[12][0-9]|3[01])$', input_variables) != None:
                    print("Thank you for sharing your demographic/socioeconomic variables of interest.")
                    i = 1
            except ValueError:
                print("This is not a valid input.  Please enter two values, separated by a comma.")
    
    i = 0
    #4. Ask what variables are of interest
    if input_dataType == '2': # ask what kind of plot
        while i == 0:
            plot_type = input("\nWould you like to plot a time series, comparison, or both?\n1. Time Series.\n2. Comparison.\n3. Both.\n (Please type a 1, 2, or 3 and press enter.)")
            try:
                if re.search(r'^[1-3]$', plot_type) != None:
                    print("Thank you for choosing your desired plot type.")
                    i = 1
            except ValueError:
                print("This is not a valid input.  Please enter one integer.")
    
    var_dict = {
            1:'estab', 
            2:'emp', 
            3:'empszes', 
            4:'price', 
            5:'rent',
            6:'rentpersqft', 
            7:'poverty', 
            8:'unemployment',
            9:'total_pop_both', 
            10:'white_both', 
            11:'black_both', 
            12:'american_indian_both',
            13:'asian_both', 
            14:'hawaiian_both', 
            15:'two_or_more_races_both',
            16:'total_pop_male', 
            17:'white_male', 
            18:'black_male', 
            19:'american_indian_male',
            20:'asian_male', 
            21:'hawaiian_male', 
            22:'two_or_more_races_male',
            23:'total_pop_female', 
            24:'white_female', 
            25:'black_female',
            26:'american_indian_female', 
            27:'asian_female', 
            28:'hawaiian_female',
            29:'two_or_more_races_female'}
    
    
    
    var_dict_clean = {
            1:'Number of Business Establishments', 
            2:'Number of Employees', 
            3:'Employment Size of Establishments', 
            4:'Average Housing Price ($)', 
            5:'Average Rent Price ($)',
            6:'Average Rent per Square Foot ($/ft^2)', 
            7:'Number of Citizes in Poverty', 
            8:'Unemployment Rate (%)',
            9:'Total Population', 
            10:'Total White Population', 
            11:'Total Black Population', 
            12:'Total American Indian Population',
            13:'Total Asian Population', 
            14:'Total Hawaiian Population', 
            15:'Total Population with one or more Races',
            16:'Total Male Population', 
            17:'Total White Male Population', 
            18:'Total Black Male Population', 
            19:'Total American Indian Male Population',
            20:'Total Asian Male Population', 
            21:'Total Hawaiian Male Population', 
            22:'Total Male Population with one or more Races',
            23:'Total Female Population', 
            24:'Total White Female Population', 
            25:'Total Black Female Population',
            26:'Total American Indian Female Population', 
            27:'Total Asian Female Population', 
            28:'Total Hawaiian Female Population',
            29:'Total Female Population with one or more Races'}
    
    #END USER INPUT
    
    
    #EXTRACT RELEVANT DATA BASED ON USER INPUT
    
    # extract cities
    wanted_cities = [] # define new list
    input_region_vals = str(input_regions).split(',') # make input table variables iterable
    for key in regions_dict:
        for var in input_region_vals:
            if str(key) == str(var):
                wanted_cities.append(regions_dict[key])
    if wanted_cities == ["All"]:
        wanted_cities = [city for city in regions_dict.values() if city != "All"]
        
    # extract variables
    wanted_vars = [] # define new list
    input_variable_vals = str(input_variables).split(',') # make input table variables iterable
    for key in var_dict:
        for var in input_variable_vals:
            if str(key) == str(var):
                wanted_vars.append(var_dict[key])
                   
    wanted_mergedDF = mergedDF[['year','city_x','state'] + wanted_vars]
    if wanted_cities[0] != 'All':
        wanted_mergedDF = wanted_mergedDF[wanted_mergedDF.apply(lambda x: x['city_x'] in wanted_cities, axis=1)]
        
    #END EXTRACT RELEVANT DATA BASED ON USER INPUT
    
    print("\n\nBelow are summarized statistics of " + ", ".join(wanted_vars) + " in the cities " + ", ".join(wanted_cities) + "\n")
    
    #START TABLE GENERATION
    print(wanted_mergedDF.describe())
    #END TABLE GENERATION
    
    #START PLOT/TABLE GENERATION
    pylab.rcParams['figure.figsize'] = (12.0, 8.0) #figure sizing
    def goBar(yVar,listCities):
        yIdx = [k for k,v in var_dict.items() if v == yVar][0]
        cleanY = var_dict_clean[yIdx]
        print(cleanY + " Trends in " + ", ".join(listCities) + " between 2014-2017:")
        labels = list(wanted_mergedDF["year"].unique())
        x = np.arange(len(labels))  # the label locations
        width = 0.1  # the width of the bars
        fig, ax = plt.subplots()
        totBars = len(listCities)
        weight = -1*(totBars / 2) + 0.5
        for city in listCities:
            yList = list(wanted_mergedDF.loc[wanted_mergedDF['city_x'] == city][yVar])
            ax.bar(x - weight * width, yList, width, label=city)
            weight += 1
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel("Year")
        ax.set_ylabel(cleanY)
        ax.set_title(cleanY + ' by Year')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        fig.tight_layout()
        plt.show()
        
    def goScat(listVars,listCities):
        x = listVars[0]
        y = listVars[1]
        xIdx = [k for k,v in var_dict.items() if v == x][0]
        cleanX = var_dict_clean[xIdx]
        yIdx = [k for k,v in var_dict.items() if v == y][0]
        cleanY = var_dict_clean[yIdx]
        print(cleanY + " vs. " + cleanX + " in " + ", ".join(listCities) + " between 2014-2017:")
        fig, ax = plt.subplots()
        markerList = ['#EE4266','#2A1E5C','#F0C262','#9A9E9D','#3CBBB1']
        lineList = ['#ED8EA2','#7C7CD8','#F0C29D','#C4CBCA','#C9F2EE']
        n = 0
        for city in listCities:
            plotDF = wanted_mergedDF.loc[wanted_mergedDF['city_x'] == city]
            plotDF = plotDF.sort_values(by=[x])
            ax.plot(x,y, data=plotDF, marker='o', markerfacecolor=markerList[n], markersize=12, 
                     color=lineList[n], linewidth=4, label=city)
            n += 1
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel(cleanX)
        ax.set_ylabel(cleanY)
        ax.set_title(cleanY + ' vs ' + cleanX)
        plt.legend()
        plt.show()
    
    if input_dataType == '2': #if plot visualization was chosen
        if plot_type in ['1','3']:
            for metric in wanted_vars:
                goBar(metric,wanted_cities)
        if plot_type in ['2','3']:
            goScat(wanted_vars,wanted_cities)
    else: #display table
        print("Below is a table view of " + ", ".join(wanted_vars) + " in the cities " + ", ".join(wanted_cities) + "\n")
        pd.options.display.width=None
        pd.options.display.max_columns = None
        print(wanted_mergedDF)
    #END PLOT/TABLE GENERATION
    
    #ASK USER IF INTERESTED IN ADDITIONAL ANALYSIS
    i = 0
    while i == 0:
        note = ""
        if input_priceModel == "2":
            note = "Note: Additional analysis is charged based on the query-level pricing terms."
            
        restart = input("\nWould you like to continue your analysis? " + note + "\n1. Yes.\n2. No.\n (Please type a 1 or 2 and press enter.)")
        try:
            if re.search(r'^[1-2]$', restart) != None:
                print("Thank you for your response.")
                i = 1
                if restart == "2":
                    end = 1
        except ValueError:
            print("This is not a valid input.  Please enter either '1' or '2'.")  
    #END REQUEST FOR ADDITIONAL ANALYSIS
#loops if additional analysis requested
    
#END REQUESTS FOR USER INPUT
    
#BEGIN FORECAST PLOTTING
i = 0
while i == 0:
    toForecast = input("\nWould you like to see a home value forecast for " + ", ".join(wanted_cities) + "?\n1. Yes.\n2. No.\n (Please type a 1 or 2 and press enter.)")
    try:
        if re.search(r'^[1-2]$', toForecast) != None:
            print("Thank you for your response.")
            i = 1
    except ValueError:
        print("This is not a valid input.  Please enter either 'y' or 'n'.")  
        
if toForecast == "1":   
    fullData = pd.read_csv('./CompiledData/forecastData.csv')
    fullData.iloc[:,0] = pd.to_datetime(fullData.iloc[:,0], format = '%Y-%m')
    fullData.set_index(fullData.columns[0], inplace = True)
    
    for col in fullData.columns: #filter out cities that are not of interest
        if col not in wanted_cities:
            del fullData[col]
            
    fullData.plot()
    plt.axvline(x=fullData.index[-12], color='black')
    plt.xlabel('Year')
    plt.ylabel('Average House Value [USD]')
    plt.title('Average House Value [USD] 1996-2019 including 2020 Forecast')
    plt.show()
    
    fullData[-120:].plot()
    plt.axvline(x=fullData.index[-12], color='black')
    plt.xlabel('Year')
    plt.ylabel('Average House Value [USD]')
    plt.title('Average House Value [USD] 2011-2019 including 2020 Forecast')
    plt.show()

#END FORECAST PLOTTING

