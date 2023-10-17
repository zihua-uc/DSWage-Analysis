"""
This file is the main execution file of the python files in this repository.
When running this file in the terminal, it requires 5 boolean arguments, that 
matches which individual files to execute. Each arguments corresponds to the 
file execution order: Glassdoor scraper -> ACS scraper -> Clean data -> Plot basic analysis
-> Run detailed OLS regression
Look at README.md for details.
"""

# import python files in this repo
import sys
import state_job_scrape
import Glassdoor_scraper
import ACS_scraper
import data_cleaner
import analysis_plot

# import necessary library to run R file
import subprocess
 
if __name__ == "__main__":
    # print the name of this file
    print("\nName of Python script:", sys.argv[0])
    
    print("\nExecuting Files:")

    print(f"\nUrl Job count Scraper: {sys.argv[1]}")
    # if first argument is True, execute the url/job count scraping file
    if sys.argv[1] == 'True':
        print("Running Url Job count Scraper...")
        state_job_scrape
    
    print(f"\nGlassdoor Scraper: {sys.argv[2]}")
    # if second argument is True, execute the Glassdoor scraping file
    if sys.argv[2] == 'True':
        print("Running Glassdoor Scraper...")
        Glassdoor_scraper

    print(f"\nACS Scraper: {sys.argv[3]}")
    # if third argument is True, execute the ACS scraping file
    if sys.argv[3] == 'True':
        print("Running ACS Scraper...")
        ACS_scraper

    print(f"\nData Cleaner: {sys.argv[4]}")
    # if fourth argument is True, execute the data cleaning file
    if sys.argv[4] == 'True':
        print("Running Data Cleaner...")
        data_cleaner

    print(f"\nAnalysis Plotting: {sys.argv[5]}")
    # if fifth argument is True, execute the result plotting file
    if sys.argv[5] == 'True':
        print("Plotting Analysis Result...")
        analysis_plot

    print(f"\nRegression Runner: {sys.argv[6]}")
    # if sixth argument is True, execute the OLS regression file in R
    if sys.argv[6] == 'True':
        print("\nRunning R Subprocess...")
        # Change accordingly to your Rscript.exe & R script path
        # this is the default path for mac
        r_path = "/usr/local/bin/Rscript"
        script_path = "Regressions.R"
        # Execute command
        cmd = [r_path, script_path]
        subprocess.check_output(cmd, universal_newlines=True)
        
    print("\n\nExecution Complete")
