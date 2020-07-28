# r.o.py
I developed this project while taking Data Focused Python during my Masters program at Carnegie Mellon University. It utilizes the Zillow API, the U.S. Census API, and USDA CSV exports to build visualizations that illustrate the correlations between socioeconomic influences and real estate metrics across several U.S. cities with varying demographics.

To setup and run the R.O.Py. program, please execute the following:
1.	Download the provided “SectionD3_Group1_ProjectFinal_SourceCode.zip” file and extract the contents to a folder of choice.  Then, extract the “sourceCode.zip” contents to a base folder.
2.	Watch the provided instruction video (“ROPy Tutorial.mp4”).
3.	Ensure that that clean.py, vis.py, and unemploymentScrape.py. and chromedriver.exe remain in the base folder while the “DataFocusedPython_Group1_RAW.xlsx” file resides within the CompiledData folder.
a.	Add driver to PATH environment (PATH variable must be extended by "{path to folder}\chromedriver.exe") or manually specify the location of the “chromedriver.exe” file in lines 26 and 54 of the unemploymentScrape.py file. 
4.	Ensure that all libraries listed at the top of clean.py and vis.py are installed (e.g. pandas, re, matplotlib.pyplot, numpy, datetime, requests, selenium, statsmodels, sklearn, math, pylab).
5.	Run vis.py in Spyder (via the Anaconda IDE).
a.	Execute the commands listed in Case 1 below.
6.	Run vis.py again.
a.	Execute the commands listed in Case 2 below.

Question	Case 1: License User with Table Output	Case 2: Query-Level User with Plot Output
Would you like to reload the data, or use the existing data frame?
1. Rerun
2. Use existing data	1 
(NOTE: Option 1 will run the web-scraping function, which takes ~20 minutes to complete) 	2
What pricing model would you like to utilize?
1. Annual License
2. Query Level	1	2
What region(s) would you like to evaluate?
1. New York City, NY 
2. Pittsburgh, PA
3. San Francisco, CA
4. Wausau, WI
5. Charleston, SC	N/A	2,3,5
How would you like for your data to be displayed?
1. Table
2. Plot	1	2
What demographic/socioeconomic variables would you like to evaluate? (choices 1 - 29)	1,5,8,9,16,20,22,24	N/A
What demographic/socioeconomic variables would you like to plot? (choices 1 - 29)	N/A	1,4
Would you like to plot a time series, comparison, or both?
1. Time Series
2. Comparison
3. Both	N/A	3
Would you like to continue your analysis?
1. Yes
2. No	2	2
Would you like to see a home value forecast?
1. Yes
2. No	1	2

NOTE: Typically, a separate series of questions would be asked to the customer in the case that the one-on-one consulting business model was selected.  However, considering this model would require responses for many open-ended questions, we decided to provide standardized predictive analyses for estimated housing prices for each specified area of interest (these results are shown when the user specifies that he/she would “like to see a home value forecast”).  More information regarding the design, setup, and execution of the models can be found in the “Additional Notes” section.

Additional Notes:
Using the Scrapy library and resources provided by the GitHub project (https://github.com/adodd202/Airbnb_Scraping), we attempted to scrape Airbnb rental information for each region of interest.  However, the Airbnb information introduced the following challenges: 
●	Significant amounts of CSS elements must be filtered through to find information of interest.
●	Many settings must be fine tuned to successfully extract information, including download delay, autothrottle, price ranges of interest, and more.

After tweaking the parameters of the Python script, we were able to successfully extract rental information, including room ID, rental description, ratings, reviews, price, number of bathrooms/bedrooms/guests, latitude, longitude, and superhost status.  Unfortunately, the scraping of the website was not consistent due to scraping blockers installed by Airbnb. While the use of a VPN and changing of the IP address proved to help in some instances, the script remained unreliable.  As a result, we could not effectively utilize the Airbnb data for our project, considering:
●	The website could not be reliably scraped.
●	The website does not provide downloadable data.
●	Time series data is not accessible.  Only real-time information could be extracted.




In place of the Airbnb data, we utilize information downloaded from Zillow to predict housing prices for each region.  The following outlines the steps that were taken:
1.	Retrieve monthly time series data of house values for the 5 cities since 1996.
2.	Select model type.
a.	Decide on using a time series model. 
b.	Use the Dickey Fuller Test to check whether the data exhibits stationarity.
■	Log transpose the data, take first differences, and perform time series decomposition.
c.	Realize better stationarity with differencing and select Auto-Regressive Integrated Moving Average (ARIMA) as the preferred model.
d.	Use autocorrelation and partial autocorrelation to define meaningful p,q parameters for the ARIMA(p,1,q) model.
3.	Train the model on 80% of the data and validate with the remaining 20%.
4.	Perform out-of-sample forecast for the monthly house values in 2020.
a.	For out-of-sample forecasts, train on 100% of the data and predict for the next 12 months.
5.	Store historical values and the forecasted values in one comprehensive data frame.
6.	Plot results.

NOTE: The time series data for average home prices for all cities since 1996 with the 1-year forecast was stored in a .csv file.  This allows for the predicted results to be quickly loaded and retrieved within the R.O.Py. program when a user submits a request for a model out.  We understand that a scheduled task would need to be in place to retrain the model in a production environment to ensure that the predictive results are based on the most up to date information.

While we understand that more information would need to be extracted and analyzed to increase the accuracy of the prediction, we believe that this use case showcases the value-added possibilities that the aggregated demographic, socioeconomic, and housing data within R.O.Py. can supply.


