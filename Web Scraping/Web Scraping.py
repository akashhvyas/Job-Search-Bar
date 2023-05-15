import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

service = Service('C:/Users/Mi/Downloads/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'C:/Users/Mi/Downloads/chromedriver_win32/chromedriver.exe')

link = 'https://www.instahyre.com/search-jobs/'

driver.get(link)

company = []
designation = []
locations = []
estab_year = []
employees_count = []
skills = []
link = []
while True:
    data = driver.find_elements(By.CLASS_NAME, 'employer-row')
    for datas in data:
        try:
            Job_role = datas.find_element(By.CLASS_NAME,'employer-job-name').text
            company_name = Job_role.split(' - ')[0]
            position = Job_role.split(' - ')[1]
            company.append(company_name)
            designation.append(position)
        except:
            company.append(np.nan)
            designation.append(np.nan)
        try:
            location = datas.find_element(By.CLASS_NAME,'employer-locations').text
            if len(location)>50:
                loc = location[54:]
                locations.append(loc)
            else:
                loc = location.split("in")[1].strip()
                locations.append(loc)
        except:
            locations.append(np.nan)
        try:
            est_yr = datas.find_element(By.CLASS_NAME,'employer-info').text
            established_year = est_yr.split("•")[0][-5:]
            comapny_size = est_yr.split("•")[1].strip()
            estab_year.append(established_year)
            employees_count.append(comapny_size)
        except:
            estab_year.append(np.nan)
            employees_count.append(np.nan)

        # Extract job skills
        try:
            skill_list = datas.find_element(By.CSS_SELECTOR, '.job-skills ul')
            skills_text = []
            for skill in skill_list.find_elements(By.TAG_NAME, 'li'):
                skills_text.append(skill.text)
            skills.append(', '.join(skills_text))
        except:
            skills.append(np.nan)

        # time.sleep(1)

        try:
            links = datas.find_element(By.XPATH,'.//*[@id="employer-profile-opportunity"]')
            url = links.get_attribute('href')
            link.append(url)
        except:
            link.append(np.nan)

    print(len(company))
    try:
        next_button = driver.find_element(By.XPATH, './/*[@id="job-function-page"]/div[2]/div/div[1]/div[1]/div[11]/li[12]')
        next_button.click()
        time.sleep(2)
    except:
        print("PAGE END")
        break



df = pd.DataFrame({'Company': company,
                   'Designation': designation,
                   'Locations': locations,
                   'Established Year': estab_year,
                   'Employees Count': employees_count,
                   'Skills': skills,
                   'Link': link})

df.to_csv(r'A:/Masai Projects/Job Analytics project/Job_Data1.csv',index = False)
print(df)