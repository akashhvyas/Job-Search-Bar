import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


df = pd.read_csv("A:/Masai Projects/ML Project Job ANAlytics/Job_Data.csv")
df.dropna(inplace=True)
df.to_csv("A:/Masai Projects/ML Project Job ANAlytics/Job_Datacleaned.csv",index=False)


Link_L = []
for i in df['Link']:
    Link_L.append(i)
service = Service('C:/Users/Mi/Downloads/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(executable_path=r'C:/Users/Mi/Downloads/chromedriver_win32/chromedriver.exe')

HR_name = []
Experience = []

# link = 'https://www.instahyre.com/job-245061-data-scientist-engineering-at-google-2-bangalore-hyderabad/'
try:
    for link in Link_L:
        driver.get(link)
        try:
            hr_name = driver.find_element(By.CLASS_NAME,"rec-name").text
            HR_name.append(hr_name)
            time.sleep(2)
        except:
            HR_name.append("NA")
        print(len(HR_name))

        try:
            exp = driver.find_element(By.XPATH,'//*[@id="floating-header"]/div[1]/div/span[2]').text
            Experience.append(exp)
        except:
            Experience.append("NA")
        

except:
    print("NA")

df = pd.DataFrame({"HR_Name":HR_name,"Experience":Experience})

df.to_csv("A:/Masai Projects/Job Analytics project/hr_exp.csv",index = False)
print(df)