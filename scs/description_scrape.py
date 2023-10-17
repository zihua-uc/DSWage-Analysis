"""
This file is the scraper that scrapes the details when navigated to the job-level
url. The details include: salary, job rating, job location, jog role, HQ location,
url, etc.
This code is referenced from the 'glassdoor-scraper' repository by 
kelvinxuande.
"""

from time import sleep
import random
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup


# checks and corrects the scheme of the requested url
def checkURL(requested_url):
    """
    If the requested_url does not have a scheme (i.e., start with http or https)
    then add the https scheme
    """
    if not urlparse(requested_url).scheme:
        requested_url = "https://" + requested_url
    return requested_url
        
             
# fetches data from requested url and parses it through beautifulsoup
def getAndParse(driver, requested_url):
    """
    Navigate to the requested url, click on the company tab, and beautiful
    soup the page html
    """
    requested_url = checkURL(requested_url)
    try:
        driver.get(requested_url)
        sleep(random.uniform(10.23, 19.41))
        try:
            driver.find_element(By.XPATH, "//*[text()='Company']").click()
        except Exception as e:
            print(e)
        src = driver.page_source
        page_soup = soup(src, 'lxml')
        return page_soup, requested_url

    except Exception as e:
        print(e)


# extracts desired data from listing banner
def extract_listingBanner(listing_soup):
    """
    Extract job listing information that is found in the banner, i.e., 
    company name, company star rating, name of job listing offered role,
    location of the job listing, and job listing estimated salary
    """
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div",
                                                class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        companyName = "NA"
        company_starRating = "NA"
        company_offeredRole = "NA"
        company_roleLocation = "NA"
    
    if listing_bannerGroup_valid:
        try:
            company_starRating = listing_bannerGroup.find(
                                                "span",
                                                class_="css-1pmc6te e11nt52q4")\
                                                    .getText()
        except:
            company_starRating = "NA"
        if company_starRating != "NA":
            try:
                companyName = listing_bannerGroup.find(
                                                "div",
                                                class_="css-16nw49e e11nt52q1")\
                                                    .getText()\
                                                    .replace(company_starRating,
                                                             '')
            except:
                companyName = "NA"
            company_starRating = company_starRating[:-1]
        else:
            try:
                companyName = listing_bannerGroup.find(
                                                "div",
                                                class_="css-16nw49e e11nt52q1")\
                                                    .getText()
            except:
                companyName = "NA"

        try:
            company_offeredRole = listing_bannerGroup.find(
                                                "div",
                                                class_="css-17x2pwl e11nt52q6")\
                                                    .getText()
        except:
            company_offeredRole = "NA"

        try:
            company_roleLocation = listing_bannerGroup.find(
                                                "div",
                                                class_="css-1v5elnn e11nt52q2")\
                                                    .getText()
        except:
            company_roleLocation = "NA"

        try:
            company_salary = listing_bannerGroup.find(
                                        "span",
                                        class_="small css-10zcshf e1v3ed7e1")\
                                            .getText()
        except:
            company_salary = "NA"
            
    return companyName, company_starRating, company_offeredRole, \
        company_roleLocation, company_salary


# extracts desired data from company info
def extract_companyInfo(listing_soup):
    """
    Extract company information such as company HQ location, year company was
    founded, industry company is in, company annual revenue, company size,
    company type, sector that company is in
    """
    listing_companyInfo_valid = False
    try:
        listing_companyInfo_group = listing_soup.find("div", {'id': 'InfoFields'})
        listing_companyInfo_valid = True
    except:
        print("[ERROR] Error occurred in function extract_companyInfo")
        companyHQ = "NA"
        company_founded = "NA"
        company_industry = "NA"
        company_revenue = "NA"
        company_size = "NA"
        company_type = "NA"
        company_sector = "NA"
    
    if listing_companyInfo_valid:
        try:
            companyHQ = \
                listing_companyInfo_group.find("span", 
                                                {"id": "headquarters"}
                                                ).getText()
        except:
            companyHQ = "NA"
        try:
            company_founded = \
                listing_companyInfo_group.find("span", 
                                                {"id": "yearFounded"}
                                                ).getText()
        except:
            company_founded = "NA"
        try:
            company_industry = \
                listing_companyInfo_group.find("span", 
                                                {"id": 
                                                 "primaryIndustry.industryName"
                                                 }).getText()
        except:
            company_industry = "NA"
        try:
            company_revenue = \
                listing_companyInfo_group.find("span", 
                                                {"id": "revenue"}
                                                ).getText()
        except:
            company_revenue = "NA"
        try:
            company_size = \
                listing_companyInfo_group.find("span", 
                                                {"id": "size"}
                                                ).getText()
        except:
            company_size = "NA"
        try:
            company_type = \
                listing_companyInfo_group.find("span", 
                                                {"id": "type"}
                                                ).getText()
        except:
            company_type = "NA"
        try:
            company_sector = \
                listing_companyInfo_group.find("span", 
                                                {"id": 
                                                 "primaryIndustry.sectorName"
                                                 }).getText()
        except:
            company_sector = "NA"
             
    return (companyHQ, company_founded, company_industry, company_revenue, 
            company_size, company_type, company_sector)


# extract data from listing
def extract_listing(driver, url):
    """
    Extract all relevant information from given url
    """
    request_success = False

    try:
        listing_soup, requested_url = getAndParse(driver, url)
        request_success = True
        
    except Exception as e:
        print("[ERROR] Error occurred in extract_listing, requested url: \
              {} is unavailable.".format(url))
        return ("NA", "NA", "NA", "NA", "NA", "NA")

    if request_success:
        companyName, company_starRating, company_offeredRole, \
            company_roleLocation, company_salary \
                = extract_listingBanner(listing_soup)
        companyHQ, company_founded, company_industry, company_revenue, \
            company_size, company_type, company_sector \
                = extract_companyInfo(listing_soup)
        
        rv = (companyName, company_starRating, company_offeredRole, 
              company_roleLocation, company_salary, companyHQ, company_founded, 
              company_industry, company_revenue, company_size, company_type, 
              company_sector, requested_url)

        return rv


# extract listing urls
def extract_listings_url(page_soup):
    """
    Get urls of all job listings from a glassdoor search page
    """
    # this is slower but more robust:
    # get all links regardless of type and extract those that match
    listings_list = list()

    for a in page_soup.find_all('a', href=True):
        if "/partner/jobListing.htm?" in a['href']:
            listings_list.append("www.glassdoor.com" + a['href'])

    listings_set = set(listings_list)
    jobCount = len(listings_set)

    try:
        assert jobCount != 0
    except Exception as e:
        print(e)
        print("[ERROR] Assumptions invalid")

    return listings_set, jobCount
