"""
This code scrapes the ACS census data from its API and saves it into a file in
the 'data' folder.
"""

import pandas as pd
import requests
import json


def ACS_data_fetch(state_codes):
    """
    DP02_0018E: Population in households
    Estimate!!RELATIONSHIP!!Population in households

    DP02_0068PE: percentage of college or higher
    Percent!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher

    DP03_0039PE: percent employed in the information industry
    Percent!!INDUSTRY!!Civilian employed population 16 years and over!!Information

    DP03_0062E: Median income
    Estimate!!INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars)

    DP04_0101E: Median monthly house owner cost
    Estimate!!SELECTED MONTHLY OWNER COSTS (SMOC)!!Housing units with a mortgage!!Median (dollars)

    DP04_0134E: Median gross rent
    Estimate!!GROSS RENT!!Occupied units paying rent!!Median (dollars)
    """

    ACS_key = "2553c9516571a4f907de1e2a681c76bc8ff025fe"
    req_fields = ["DP02_0018E", "DP02_0068PE", "DP03_0039PE", "DP03_0062E",
                  "DP04_0101E", "DP04_0134E"]
    req_url = f"https://api.census.gov/data/2021/acs/acs1/profile?get=NAME,{','.join(req_fields)}&for=state:*&key={ACS_key}"
    response = requests.get(req_url).json()

    state_codes_df = pd.DataFrame(state_codes)
    state_codes_df.columns = ['state','abbrev']

    df = pd.DataFrame(response[1:],columns=response[0])
    df = df.merge(state_codes_df, on='state')
    df.columns = ['state_name',
                'state_pop_in_hh',
                'state_pct_college',
                'state_pct_emp_tech',
                'state_med_income',
                'state_med_owner_cost',
                'state_med_rent',
                'state_code',
                'state']
    df.to_csv('../data/ACS_data.csv', index=False)


if __name__ == "__main__":
    state_codes = [["01", "AL"], ["02", "AK"], ["04", "AZ"], ["05", "AR"], 
                ["06", "CA"], ["08", "CO"], ["09", "CT"], ["10", "DE"], 
                ["11", "DC"], ["12", "FL"], ["13", "GA"], ["15", "HI"], 
                ["16", "ID"], ["17", "IL"], ["18", "IN"], ["19", "IA"], 
                ["20", "KS"], ["21", "KY"], ["22", "LA"], ["23", "ME"], 
                ["24", "MD"], ["25", "MA"], ["26", "MI"], ["27", "MN"], 
                ["28", "MS"], ["29", "MO"], ["30", "MT"], ["31", "NE"], 
                ["32", "NV"], ["33", "NH"], ["34", "NJ"], ["35", "NM"], 
                ["36", "NY"], ["37", "NC"], ["38", "ND"], ["39", "OH"], 
                ["40", "OK"], ["41", "OR"], ["42", "PA"], ["44", "RI"], 
                ["45", "SC"], ["46", "SD"], ["47", "TN"], ["48", "TX"], 
                ["49", "UT"], ["50", "VT"], ["51", "VA"], ["53", "WA"], 
                ["54", "WV"], ["55", "WI"], ["56", "WY"], ["72", "PR"]]
    ACS_data_fetch(state_codes)
