from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pandas as pd
import sys
import time
import json

# Using fake user agents
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=options, executable_path='Chrome Driver/chromedriver')# Launch Chrome web driver

# get username & password from terminal launch command, as well as json output path
username = sys.argv[1]
password = sys.argv[2]


# connect to applied jobs page
driver.get('https://myjobs.indeed.com/applied?hl=en&co=US&from=_atweb_gnav-jobsearch--jasx')

# login
inputElement = driver.find_element_by_id("login-email-input")
inputElement.send_keys(username)
inputElement = driver.find_element_by_id("login-password-input")
inputElement.send_keys(password)
inputElement.submit()
print("Press any key when you've completed the captcha")
input()

# Get two lists, one for the app cards and one for the job locations
appCards = driver.find_elements_by_xpath('//div[contains(@class, "atw-AppCard")]')
locations = driver.find_elements_by_xpath('//div[contains(@class, "atw-JobInfo-companyLocation")]')
count = 0

# Create list variables to be filled
dataIds = []
links = []
job_titles = []
companys = []
remote = []

# Traverse through each app card, retrieve and save job data id, link, and title
for appCard in appCards:
	dataid = appCard.get_attribute('data-id')
	
	if dataid != None:
		currentCard = driver.find_element_by_xpath(f'//div[contains(@data-id, "{dataid}")]')
		dataIds.append(dataid)
		links.append('https://www.indeed.com/viewjob?jk=' + dataid + '&hl=en')
		hrefCard = currentCard.find_element_by_xpath(f'//a[contains(@href, "https://www.indeed.com/viewjob?jk={dataid}&hl=en")]')
		job_titles.append(hrefCard.text.split("\n", 1)[0])

# For each location, retrieve and save the hiring company and whether or not the job is remote
for location in locations:
	companys.append(location.text.split("\n", 1)[0])
	remote.append(1) if ("Remote" in location.text or "REMOTE" in location.text or "Remote" in job_titles[count] or "REMOTE" in job_titles[count]) else remote.append(0)
	print(job_titles[count])
	count += 1
print(companys)
print(remote)

# Save variables to a pandas DataFrame and export it as a csv file
df = pd.DataFrame(
	{'job_title' : job_titles,
	'data_id' : dataIds,
	'company' : companys,
	'remote' : remote,
	'link' : links
	})

df.to_csv('jobs.csv', index=False)

print("Saved above data as jobs.csv.")