"""
This file is the main scraper file for scraping Glassdoor data.
This file runs the state_job_scrape.py and get urls for the state-level search.
Then it runs the extract_dec.py to navigate to the state-level search url and
scrape the url of the job listings under the state-level search.
Finally, the code navigates to the job listings url and scrapes the necessary
"""

import csv
import os
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import description_scrape
import json


def fileWriter(listOfTuples, output_fileName):
    """
    writes the output into a csv file at the designated folder

    Inputs:
        listOfTuples (list): the data that is to be saved
        output_fileName (string): path and filename where the data is saved
    """
    with open(output_fileName,'a', newline='') as out:
        csv_out = csv.writer(out)
        for row_tuple in listOfTuples:
            try:
                csv_out.writerow(row_tuple)
                # can also do csv_out.writerows(data) instead of the for loop
            except Exception as e:
                print("[WARN] In filewriter: {}".format(e))


# main scraping function
def glassdoor_scraper(driver, base_url, target_num, state_search, output_fileName):
    """
    Inputs:
        driver (webdriver object): the Chrome webdriver object
        base_url (str): the url to start the search from (state-level search url)
        target_num (int): the maximum number of jobs in the state-level search
        state_search (str): the name of the state it is scraping
        output_fileName (str): the path to save the output
    """
    # initialise variables
    page_index = 1
    total_listingCount = 0

    while total_listingCount <= int(target_num):
        # clean up buffer
        list_returnedTuple = []
        driver.get(base_url)
        sleep(random.uniform(10.11, 14.86))
                
        starting_page = 5
        while page_index > starting_page:
            driver.find_element(
                By.XPATH, 
                "//*[@id='MainCol']/div[2]/div/div[1]//*[text()={}]"
                .format(starting_page)).click()
            sleep(random.uniform(3, 4))
            starting_page += 2
            
        driver.find_element(By.XPATH, 
                            "//*[@id='MainCol']/div[2]/div/div[1]//*[text()={}]"
                            .format(page_index)).click()
        sleep(random.uniform(3, 4))
        src = driver.page_source
        page_soup = soup(src, 'lxml')
        current_page = page_soup.find(
            "button", 
            {"class": "page selected css-1hq9k8 e13qs2071"}
            ).getText()
        assert current_page == str(page_index)
        listings_set, jobCount = description_scrape.extract_listings_url(page_soup)
        
        print("\n[INFO] Processing page index {}: {}"
              .format(page_index, base_url))
        print("[INFO] Found {} links in page index {}"
              .format(jobCount, page_index))

        for listing_url in listings_set:
            # to implement cache here
            returned_tuple = description_scrape.extract_listing(driver, listing_url)
            returned_tuple = (*returned_tuple, state_search)
            list_returnedTuple.append(returned_tuple)

        fileWriter(listOfTuples=list_returnedTuple, 
                   output_fileName=output_fileName)

        # done with page, moving onto next page
        total_listingCount = total_listingCount + jobCount
        print("[INFO] Finished processing page index {}; \
              Total number of jobs processed: {}"
              .format(page_index, total_listingCount))
        page_index = page_index + 1


##################################################################
######################### main execution #########################
##################################################################

if __name__ == "__main__":
    with open('../data/state_url.txt') as f:
        state_url = f.read().splitlines()

    with open('../data/state_jobs_count.json', 'r') as f:
        job_count_dict = json.load(f)

    # initialises output directory and file
    if not os.path.exists('data'):
        os.makedirs('data')
    # write the results into the output file
    output_fileName = "../data/job_search_data.csv"
    csv_header = [("companyName", "company_starRating", "company_offeredRole", 
                "company_roleLocation", "company_salary", "companyHQ", 
                "company_founded", "company_industry", "company_revenue", 
                "company_size", "company_type", "company_sector", 
                "requested_url", "search_state")]
    # write the headers to the file
    fileWriter(listOfTuples=csv_header, output_fileName=output_fileName)

    # webdriver option to not open chrome UI when scraping
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    # if Chrome webdriver is not in yout PATH
    # driver = webdriver.Chrome(executable_path="/path/to/chrome/webdriver", options=options)

    # run the scraper python code
    for i, st in enumerate(job_count_dict):
        print("Scraping state No. {}: {}".format(i, st))
        try:
            glassdoor_scraper(driver, state_url[i], job_count_dict[st], st, output_fileName)
        except Exception as e:
            print(e)
            print("[NOTE] Moving on to next state: ")
