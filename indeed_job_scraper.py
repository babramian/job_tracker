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

# Using fake user agents
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=options, executable_path='Chrome Driver/chromedriver')# Launch Chrome web driver

# get username & password from terminal launch command
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

# find 
appCards = driver.find_elements_by_xpath('//div[contains(@class, "atw-AppCard")]')
locations = driver.find_elements_by_xpath('//div[contains(@class, "atw-JobInfo-companyLocation")]')
count = 0
dataIds = []
links = []
job_titles = []
companys = []
remote = []
for appCard in appCards:
	dataid = appCard.get_attribute('data-id')
	
	if dataid != None:
		currentCard = driver.find_element_by_xpath(f'//div[contains(@data-id, "{dataid}")]')
		dataIds.append(dataid)
		links.append('https://www.indeed.com/viewjob?jk=' + dataid + '&hl=en')
		hrefCard = currentCard.find_element_by_xpath(f'//a[contains(@href, "https://www.indeed.com/viewjob?jk={dataid}&hl=en")]')
		job_titles.append(hrefCard.text.split("\n", 1)[0])


for location in locations:
	companys.append(location.text.split("\n", 1)[0])
	remote.append(1) if ("Remote" in location.text or "REMOTE" in location.text or "Remote" in job_titles[count] or "REMOTE" in job_titles[count]) else remote.append(0)
	print(job_titles[count])
	count += 1
print(companys)
print(remote)