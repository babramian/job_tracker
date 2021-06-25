from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('Chrome Driver/chromedriver')

driver.get('https://myjobs.indeed.com/applied?hl=en&co=US&from=_atweb_gnav-jobsearch--jasx')

