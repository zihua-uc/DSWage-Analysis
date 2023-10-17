"""
This file scrapes the url whem searching for "data science" jobs for a given state.
It also scrapes the number of possible jobs in that search.
Finally, if necessary, it provides a function to save the results in a .txt and
.json file under the "data" folder.
"""

import re
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def url_job_scrpae(states_lst):
    """
    Scrape the url of the search result for  "data science" jobs for each US
    states, and the number of provided jobs for each search.
    Inputs:
        states_lst (list): the list of states in the US
    Output:
        state_url (list): the list of urls of the searches
        job_count_dict (dict): the dictionary of "state: possible job number"
    """
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    # if Chrome webdriver is not in yout PATH
    # driver = webdriver.Chrome(executable_path="/path/to/chrome/webdriver", options=options)

    state_url = []
    jobs_count = []

    for state in states_lst:
        driver.get("https://www.glassdoor.com/Job/index.htm")

        # job, location search and load
        jobs_input = driver.find_element(By.XPATH,
                                         '//input[@id="KeywordSearch"]'
                                        )
        jobs_input.send_keys('data science')
        driver.find_element(By.XPATH,
                            '//input[@id="LocationSearch"]'
                            ).clear()
        loc_input = driver.find_element(By.XPATH,
                                         '//input[@id="LocationSearch"]'
                                        )
        loc_input.send_keys(state)
        search = driver.find_element(By.XPATH,
                                     '//button[@type="submit"]'
                                    )
        search.click()
        sleep(5)
        driver.switch_to.window(driver.window_handles[-1])

        # get the url
        url = driver.current_url
        state_url.append(url)

        # get the total number of job posts
        total_jobs = driver.find_element(By.XPATH,
                                         '//h1[@data-test="jobCount-H1title"]'
                                        ).text
        jobs_count.append(re.findall(r'\d+', total_jobs)[0])
        sleep(5)

    driver.quit()
    job_count_dict = dict(zip(states_lst, jobs_count))
    return state_url, job_count_dict


def save_url_job_count(state_url, job_count_dict):
    """
    Save the scrpaed url and job count dictionary into txt and json file
    Inputs:
        state_url (list): the list of urls of the searches
        job_count_dict (dict): the dictionary of "state: possible job number"
    Output:
        state_url.txt (txt): txt files of state_url
        state_jobs_count.json (json): json file of state_jobs_count
    """
    with open('../data/state_url.txt', 'w') as f:
        for line in state_url:
            f.write(f"{line}\n")

    with open('../data/state_jobs_count.json', 'w') as outfile:
        json.dump(job_count_dict, outfile)

if __name__ == "__main__":
    # some states are not in abbreviated form due to having same abbreviation as
    # famous cities. eg) LA = {Los Angeles, Louisiana}, NY = {NewYork City, NewYork State}
    states_lst = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC',
                  'Delaware, US', 'FL', 'GA', 'HI', 'IA', 'Idaho, US', 'IL',
                  'Indiana, US', 'Kansas, US', 'KY', 'Louisiana, US',
                  'Massachusetts, US', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT',
                  'NC', 'ND', 'NE', 'New Hampshire, US', 'NJ', 'NM', 'NV', 'NY',
                  'OH', 'OK', 'OR', 'PA', 'Rhode Island, US', 'SC',
                  'South Dakota, US', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI',
                  'WV', 'WY']

    state_url, job_count_dict = url_job_scrpae(states_lst)
    # save the url and job scraper to file
    save_url_job_count(state_url, job_count_dict)
