"""
This file uses the cleaned dataset and plots relevant analysis results.
The resulting plots would be saved under the "plots" folder.

######################### WLS Explanation #####################
The census_salary_reg function runs the univariate WLS for average state salary
on each census data columns.

Y (51x1): average data science jobs salary for each state
X (51x1): census data for each state
            ['Population in Households', 'Percentage of College', 
            'Percentage Employed in Information Industry', 'Median Income', 
            'Median Monthly House Owner Cost', 'Median Gross Rent']
        6 regressions are done with X as each census data.
W (51x1): number of data science jobs for each state

Formula: hat{beta} = inv(X'WX) * (X'WY)
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def salary_state_plot(salary):
    """
    compare the average DS jobs salary among the US states
    Inputs:
        salary (dataframe): the dataframe of average state data science salary
    """
    plt.figure(figsize=(10,6))
    salary.plot(kind='bar', color='#50a84b')
    plt.xlabel('States')
    plt.ylabel('Avg Salary')
    title = 'Avg Salary of Data Science Jobs for each State'
    plt.title(title)
    plt.savefig(f'../plots/{title}.png')


def ACS_descrip_stat(census, title_dict):
    """
    compare the ACS census data between the states as the descriptive statistics
    Inputs:
        census (dataframe): the mergerd dataframe with the ACS census data and 
                            the avg salary/job count data
        title_dict (dictionary): the dictionary that matches ACS column names
                                with the detailed name
    """
    for key, val in title_dict.items():
        plt.figure(figsize=(10,6))
        census.boxplot(column = key, color='#50a84b')
        plt.xlabel('Census Variables')
        plt.ylabel('Value')
        plt.xticks([1], [val])
        title = f'Descriptive Statistics for {val}'
        plt.title(title)
        plt.savefig(f'../plots/{title}.png')


def ds_job_count(census):
    """
    compare the number of data science jobs between the states
    Inputs:
        census (dataframe): the mergerd dataframe with the ACS census data and 
                            the avg salary/job count data
    """
    census = census.set_index('state')
    plt.figure(figsize=(10,6))
    census['count'].plot(kind='bar', color='#50a84b')
    plt.xlabel('States')
    plt.ylabel('Number of DS jobs')
    title = 'Number of Data Science Jobs for each State'
    plt.title(title)
    plt.savefig(f'../plots/{title}.png')


def census_salary_reg(census, title_dict):
    """
    run an univariate WLS (weighted OLS) regression with y as 'avg salary' 
    and x as each ACS census columns
    Inputs:
        census (dataframe): the mergerd dataframe with the ACS census data and 
                            the avg salary/job count data
        title_dict (dictionary): the dictionary that matches ACS column names
                                with the detailed name
    """
    # run and plot OLS result for each census dataframe columns
    for key, val in title_dict.items():
        plt.figure(figsize=(10,6))
        x = census[key].values.reshape(-1, 1)
        y = census['salary']
        linear_regressor = LinearRegression()
        # run OLS with the number of jobs of each state as weights
        linear_regressor.fit(x, y, census['count'])
        y_pred = linear_regressor.predict(x)
        # differ size of the dots of the data based on the number of jobs
        plt.scatter(x, y, census['count'], color='#50a84b')
        plt.plot(x, y_pred, color='#A88743', linewidth=1.5)
        plt.xlabel(f'{val}')
        plt.ylabel('Avg Salary')
        title = f'Avg Salary of DS Jobs and {val}'
        plt.title(title)
        plt.savefig(f'../plots/{title}.png')


def salary_jobtitle(job_salary):
    """
    Compare the avg salary of each job titles and plot by descending order
    Inputs:
        job_salary (dataframe): the grouped dataframe of avg salary by job title 
    """
    plt.figure(figsize=(10,6))
    job_salary.plot(kind='barh', color='#50a84b')
    plt.xlabel('Job Title')
    plt.ylabel('Avg Salary')
    title = 'Avg Salary by Job Title'
    plt.title(title)
    plt.savefig(f'../plots/{title}.png')


def salary_seniority(senior_salary):
    """
    Compare the avg salary of each job seniority and plot by descending order
    Inputs:
        job_salary (dataframe): the grouped dataframe of avg salary by job seniority 
    """
    plt.figure(figsize=(10,6))
    senior_salary.plot(kind='barh', color='#50a84b')
    plt.xlabel('Job Title')
    plt.ylabel('Avg Salary')
    title = 'Avg Salary by Job Level Prefix'
    plt.title(title)
    plt.savefig(f'../plots/{title}.png')


def salary_us_map(census):
    """
    Compare and plot the avg salary of each states on the map of United States
    Inputs:
        census (dataframe): the mergerd dataframe with the ACS census data and 
                            the avg salary/job count data
    """
    title = '2023 US Data Science Jobs Avg Salary'
    fig = go.Figure(data=go.Choropleth(
        locations = census['state'], 
        z = census['salary'].astype(float), 
        locationmode = 'USA-states', 
        colorscale = 'Viridis_r',
        colorbar_title = "Millions USD"
    ))
    fig.update_layout(
        title_text = title,
        geo_scope='usa'
    )
    fig.write_image(f'../plots/{title}.png', engine='kaleido')


def owner_cost_us_map(census):
    """
    Compare and plot the avg owner cost of each states on the map of United States
    Inputs:
        census (dataframe): the mergerd dataframe with the ACS census data and 
                            the avg salary/job count data
    """
    title = '2021 US Median Rent'
    fig = go.Figure(data=go.Choropleth(
        locations = census['state'], 
        z = census['state_med_owner_cost'].astype(float), 
        locationmode = 'USA-states', 
        colorscale = 'Viridis_r',
        colorbar_title = "Millions USD"
    ))
    fig.update_layout(
        title_text = title,
        geo_scope='usa'
    )
    fig.write_image(f'../plots/{title}.png', engine='kaleido')


if __name__ == "__main__":
    # open cleaned file
    df = pd.read_csv('../data/cleaned_data.csv', encoding="ISO-8859-1")
    df.drop(columns=df.columns[0], axis=1, inplace=True)

    # open the ACS census data
    census = pd.read_csv('../data/ACS_data.csv')
    census = census.drop([1])
    census_col = census.columns[1:7]

    # get average salary for each state
    salary = df.groupby(['company_roleLocation'])['company_salary'].mean()
    salary_df = salary.reset_index()
    # get the number of offered jobs for each state
    count_jobs_dist = df.groupby(['company_roleLocation'])['companyName'].count()
    # merge the above two into a single data
    dist_df = pd.DataFrame({'count': list(count_jobs_dist),
                            'salary': list(salary)}, 
                            index = salary.index)

    # merge the ACS census data and the avg salary/job count data
    census = census.merge(dist_df.reset_index().rename(
        columns={"company_roleLocation": "state"}), on='state')
    col_tit_name = ['Population in Households', 'Percentage of College', 
                    'Percentage Employed in Information Industry', 
                    'Median Income', 'Median Monthly House Owner Cost', 
                    'Median Gross Rent']
    # match the ACS data columns with the detailed explanation title
    title_dict = dict(zip(census_col, col_tit_name))

    # avg salary for each job titles by descending order
    job_salary = df.groupby(['job_title'])['company_salary'].mean()
    job_salary = job_salary.sort_values()

    # avg salary for each job seniority by descending order
    senior_salary = df.groupby(['job_seniority'])['company_salary'].mean()
    senior_salary = senior_salary.sort_values()

    # input the above data into plotting functions
    salary_state_plot(salary)
    ACS_descrip_stat (census, title_dict)
    ds_job_count(census)
    census_salary_reg(census, title_dict)
    salary_jobtitle(job_salary)
    salary_seniority(senior_salary)
    salary_us_map(census)
    owner_cost_us_map(census)
