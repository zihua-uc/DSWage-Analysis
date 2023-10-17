# Final Project: A Geographical Analysis of Data Science Salaries in the U.S.

## Team Name: Regenstein  

## Team Members:  
1. Zihua Chen, zihuachen@uchicago.edu
    * Coded the description_scrape.py and Glassdoor_scraper.py
    * Coded the Regressions.R file and generated the OLS tables, residual plots
    * Prepared analysis interpretation
    * Ran 1/3 of the glassdoor scraper file
2. Wonje Yun, wjy1993@uchicago.edu
    * Coded the state_job_scrape.py, main.py
    * Coded half of the functions in analysis_plot.py, data_cleaner.py
    * Cleaned the codes/data into separate files and sorted them out
    * Ran 1/3 of the glassdoor scraper file
3. Mingxuan He, mingxuanh@uchicago.edu
    * Coded ACS_scraper.py
    * Coded half of the functions in analysis_plot.py, data_cleaner.py
    * Prepared outline of the presentation and details
    * Ran 1/3 of the glassdoor scraper file

GitHub Repository Link: https://github.com/macs30122-winter23/final-project-regenstein.git

Presentation Link: https://docs.google.com/presentation/d/1Cper_yfRjZK__c7YxIn292FF9H3kQw3V/edit#slide=id.p1

Report Link: https://docs.google.com/document/d/1TT6yrqpJXYNmcfCKskp4852-RNLJ__Zi/edit

Video Link: https://drive.google.com/file/d/1dPu9vp_m7htVEPQ6bEsfCC0J8goWgn_S/view?usp=share_link

## Project Description
The central research question that this project aims to answer is what factors determine salaries of data scientists. Specifically, we are interested in determinants of wages that vary across geographical locations. This difference could be driven by differences in cost of living, number of qualified candidates, etc., or a combination of these factors.

Wages in the labor market are determined by market forces of demand (companies) and supply (employees). On the demand side, higher productivity (e.g., highly educated workers) in the workforce means that companies can offer higher wages by hiring fewer workers for the same level of output. On the supply side, a higher cost of living and rental would require workers to demand higher salaries. We can observe the equilibrium wages through job listings platforms such as Glassdoor. Geographical variation in these market forces allow us to examine the importance of different factors in contributing to equilibrium wages.

We scrape data science job listings on glassdoor.com and link salaries with state-varying variables from the 2021 U.S. Census Bureau API–American Community Survey. We then run univariate and multivariate regressions of salary on state-level, company-level, and job posting-level characteristics.

According to the univariate regressions, we found that every state-level variable in our dataset had a positive relationship with salaries. However, we found that after controlling for median cost of owning a home, other state-level characteristics are no longer relevant in explaining variation in data science salaries. Interestingly, we also find that two state-level characteristics are also relevant in explaining salaries, namely percentage of workers employed in tech and percentage of college graduates, even after controlling for various factors. 

## Code Execution Description
**You must download the chrome webdriver in your local machine before running this code**

**If the webdriver is in PATH run the file. Else, change the executable_path argument in the driver object as noted in line 30 in 'state_job_scrape.py' and line 132 in 'Glassdoor_scraper.py'**

**When runnging the R code, change the path to Rscript in the the 'main.py' file in your local machine**

The code that runs the projct is located inside the 'scs' folder.
1. The 'state_job_scrape.py' file would scrape the url data and job count data which is used for description scraping in 'Glassdoor_scraper.py'
2. The 'Glassdoor_scraper.py' file would execute the scraping process by using 'description_scrape.py' and the outcome from 'state_job_scrape.py' and put them into a csv file. The already scraped result is provided in 'data/job_search_data.csv'
3. The 'ACS_scraper.py' would get the necessary data from the ACS data source. The scraped result is provided in 'data/ACS_data.csv'
4. The 'data_cleaner.py' file would clean the data in the 'job_search_data.csv' and save it into 'cleaned_data.csv'. The cleaned data is provided in 'data/cleaned_data.csv'.
5. The plotting and visulaization results can be found in 'analysis_plot.py'. It would save the plots into the 'plots' folder.
6. The ols results can be run by 'Regressions.R.' It would save the outcomes in the 'reg_result' folder. To update Regressions.pdf, open Regressions.tex and run it using a tex editor

## Code Running Example
The 'scs/main.py' file would run the codes while choosing which codes to run or not. The order of the arguments corresponds to 'state_job_scrape.py', 'Glassdoor_scraper.py', 'ACS_scrape.py', 'data_cleaner.py', 'analysis_plot.py', and 'Regressions.R' respectively.
1. To ignore the state_job_scrape.py process: skip the webscraping process which takes total 51 hours
```bash
$ python main.py False True True True True True
```
2. To ignore the state_job_scrape.py and Glassdoor_scraper.py process
```bash
$ python main.py False False True True True True
```
3. Recommended execution code that ignores the timely scraping process is:
```bash
$ python main.py False False False True True True
```

## Required Libraries
This repo uses both python and R, so the libraries for both languages must be installed
### For python:
Look at 'requirements.py' for required libraries for running this repo
1. To install only the relevant libraries:
```bash
$ pip install -r requirements.txt
```
2. To generate the same conda environment:
```bash
$ conda env create -f environment.yml
```
### For R:
```r
install.packages(c('stargazer', 'lfe', 'ggplot2', 'ggpubr'))
```

## Data Sources
### Data source 1: Glassdoor
Link: https://www.glassdoor.com/Job/index.htm

Starting from this link, we scraped the search urls and job descriptions with 'state_job_scrape.py' and 'Glassdoor_scraper.py'.

### Data source 2: U.S. Census Bureau API–American Community Survey 2021  
Link: https://www.census.gov/data/developers/data-sets/acs-1year.2021.html  

To control for wage determinants for different geographical locations, we collect data at the state level from the 2021 U.S. census. We request the data table American Community Survey (ACS) 2021–Data Profiles through the U.S. Census Bureau API. For all 50 states + D.C., we collect the following data fields aggregated at the state level:

**Demographic:**  
- Population in households
- Proportion of college graduates

**Jobs:**  
- Proportion of workers employed in the tech industry
- Median income  

**Cost of living:**  
- Median monthly cost of home ownership
- Median cost to rent  

## Reference
```
@article{grimes2019geographical,
  title={Geographical variation in wages of workers in low-wage service occupations: A US metropolitan area analysis},
  author={Grimes, Donald R and Prime, Penelope B and Walker, Mary Beth},
  journal={Economic Development Quarterly},
  volume={33},
  number={2},
  pages={121--133},
  year={2019},
  publisher={SAGE Publications Sage CA: Los Angeles, CA}
}

@book{mankiw2020principles,
  title={Principles of macroeconomics},
  author={Mankiw, N Gregory},
  year={2020},
  publisher={Cengage learning}
}

@misc{kelvinxuande,
  author = {kelvinxuande},
  title = {glassdoor-scraper},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/kelvinxuande/glassdoor-scraper}}
}

@misc{ziprecruiter, 
  url={https://www.ziprecruiter.com/Salaries/What-Is-the-Average-DATA-Scientist-Salary-by-State}, 
  journal={What is the average data scientist salary by state}, 
  publisher={ZipRecruiter}, 
  author={ZipRecruiter}
}
```
