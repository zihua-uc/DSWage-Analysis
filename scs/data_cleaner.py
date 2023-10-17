"""
This file contains the cleaning process of the scraped dataset.
As a result of executing this file, the cleaned dataset would be saved to a
separate file under the "data" folder.
"""

import numpy as np
import pandas as pd
import re


def pre_process_glassdoor(df):
    """
    The pre-processing of the scraped dataset. Apply basic cleaning process before
    specified cleaning
    Inputs:
        df (dataframe): the dataframe of the glassdoor scraping result
    Outputs:
        df (dataframe): the glassdoor scraped dataframe with the cleaned result
    """
    # drop duplicates
    df = df.drop_duplicates(subset=df.columns.difference(['requested_url']))
    # drop rows with empty salary
    df = df.dropna(subset=['company_salary'])
    # drop remote jobs or jobs without designated workplace
    df = df.drop(df[df['company_roleLocation'] == 'Remote'].index)
    df = df.drop(df[df['company_roleLocation'] == 'United States'].index)
    return df


def clean_location(s):
    """
    Match the format of the job location column of the scraping result to state
    abbreviation. The format "city, state" -> "state"
    Inputs:
        s (string): string with job location info from glassdoor scraped result
    Outputs:
        state (string): the abbreviation representation of the state, or other 
                possible outputs
    """
    # the state abbreviation dictionary to match the state name
    us_state_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC"
    }
    # strip the string by ','
    loc_lst = [loc.strip() for loc in s.split(',')]
    
    # if strip has more than two outcomes ("city, state"), fetch the state
    if len(loc_lst) > 1:
        # change to abbreviation format
        state = loc_lst[1]
    # if outcome length is less than 2 ("state" or empty), return itself
    else:
        # if outcome is in the abbrev dict, return the abbrev of state
        if loc_lst[0] in us_state_abbrev.keys():
            state = us_state_abbrev[loc_lst[0]]
        # otherwise, return NaN
        else:
            state = np.nan
    return state


def clean_salary(s):
    """
    Clean the salary column in glassdoor dataset to make range ro value
    Inputs:
        s (string): string containing salary info from glassdoor scraped result
    Outputs:
        salary (int): the cleaned salary value given the input
    """
    # re find expression: $xxxK
    res = re.findall('\$\d+K',s)

    # if salary is in annual
    if len(res) >0:
        # range: take midpoint
        if len(res) == 2:
            salary = (float(res[0][1:-1]) + float(res[1][1:-1])) / 2
        # single value
        elif len(res) == 1:
            salary = float(res[0][1:-1])
        else:
            raise ValueError('More than three salary values')
        
    # if salary is in hourly
    if len(res) == 0:
        hr_res = re.findall('\$\d+\.\d+',s)
        # range: take midpoint
        if len(hr_res) == 2:
            hr_sal = (float(hr_res[0][1:]) + float(hr_res[1][1:])) / 2
        # single value
        elif len(hr_res) == 1:
            hr_sal = float(hr_res[0][1:])
        else:
            raise ValueError('More than three salary values')
        # if hourly data, convert to yearly
        salary = hr_sal * 40 * 52 / 1000   # assume 40hr/wk * 52wk/yr

    return salary


def clean_role(s):
    """
    Clean the job title column in glassdoor dataset to make range ro value
    Inputs:
        s (string): string containing job title info from glassdoor scraped result
    Outputs:
        seniority (string): the seniority of the input job title value matching 
                            the seniority dictionary
        title (string): the data-science related title of the input job title 
                        value given the job title dictionary
    """
    seniority_dict = {'senior': ['senior','sr','manager','director','principal',
                                  'staff', 'lead', 'founding'],
                  'junior': ['junior', 'jr'],
                  'intern': ['intern', 'co-op']
                  }
    job_title_dict = {'professor': ['professor','prof.','instructor','teacher'],
                'research_scientist': ['research scientist'],
                'machine_learning_engineer': ['machine learning', 'ml ','mle ',
                                               'ai ','deep learning'],
                'business_analytics': ['business analytics', 'business analyst',
                                        'business data analyst', 'business intelligence', 
                                        'bi '],
                'software_engineer': ['software engineer', 'software developer', 
                                      'SDE'],
                'data_engineer': ['data engineer', 'data architect'],
                'data_analytics': ['data analytics', 'data analyst', 'data analysis'],
                'data_science': ['data science', 'data scientist']
                }

    # extract title by matching with dict
    title = None
    for t,t_list in job_title_dict.items():
        contains_title = any([m in s.lower() for m in t_list])
        if contains_title:
            title = t
            break
    # if no match, classify as other
    if title is None:
        title = 'other title'

    # extract seniority by matching with dict
    seniority = None
    for n, n_list in seniority_dict.items():
        contains_seniority = any([m in s.lower() for m in n_list])
        if contains_seniority:
            seniority = n
    # if no match, classify as other
    if seniority is None:
        seniority = 'no prefix'

    return seniority, title



def clean_pipeline(df):
    """
    The data cleaning process as a whole
    Inputs:
        df (dataframe): the scraped glassdoor dataframe
    Outputs:
        df (dataframe): the cleaned dataframe to be used for analysis
    """
    # apply basic data cleaning process
    df = pre_process_glassdoor(df)

    # location cleaning process
    df['company_roleLocation'] = df['company_roleLocation'].apply(clean_location)
    df.loc[df['company_roleLocation'] == 'Montgomery', 'company_roleLocation'] = 'AL'
    df['company_roleLocation'] = df['company_roleLocation'].fillna(method = 'ffill')

    # salary cleaning process
    df['salary_cleaned'] = df['company_salary'].apply(clean_salary)
    # drop if below federal minimum wage
    minwage = 7.25*40*52/1000
    df = df[df['salary_cleaned']>=minwage]
    # rename salary column
    df.rename(columns={'company_salary':'company_salary_raw',
                       'salary_cleaned':'company_salary'}, 
                       inplace=True)

    # job title and seniority claening process
    # for modeling later, use pd.get_dummies() to get dummies for seniority and title (and industry?)
    seniorityf = lambda rolestr: clean_role(rolestr)[0]
    titlef = lambda rolestr: clean_role(rolestr)[1]
    # add new columns
    df['job_seniority'] = df['company_offeredRole'].apply(seniorityf)
    df['job_title'] = df['company_offeredRole'].apply(titlef)

    df = df.reset_index()
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    return df


if __name__ == "__main__":
    # load datafile and apply the cleaning process
    df = pd.read_csv('../data/job_search_data.csv', encoding="ISO-8859-1")
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    cleaned_df = clean_pipeline(df)
    # save the cleaned file
    cleaned_df.to_csv('../data/cleaned_data.csv')
