# Job Search Bar (Machine Learning)

### **INTRODUCTION**

####  This repository comprises project files concerning a Job Search Bar implemented with machine learning. The primary goals of the project were:

1. Develop a user-friendly web-based platform allowing users to search for specific skills and access relevant market trends and job postings related to those skills.
2. Employ machine learning techniques to classify job postings based on factors such as the company's LinkedIn followers and employee count.
3. Utilize Python with the Selenium library for web scraping, extracting necessary data.
4. Perform data analysis and organization using Excel and SQL to create informative tables.
5. Implement the search bar and host it using HTML, CSS, and Streamlit for seamless user interaction and experience. 


<br />

### **TABLE OF CONTENTS**

| Files/Folder | Description |
| -----------  | ----------- |
| CSV File  | This folder contains cleaned csv data files           |
| Deployment    | This folder contains files related to deployment and spell checker      |
| Graphic | This folder contains insights snapshots that are used in this Repository     |
| Web Scraping | This folder contains Jupyter notebook file & Web driver used for Web scraping   |
| Presentation | This is a powerpoint presentation file that contains all major Insights and conclusion |



<br />

### **PROJECT ROADMAP**

<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/PowerPoint%20Presentation%20-%20Google%20Chrome%2016-05-2023%2000_01_36.png"  width="864" height="470" />

<br />

### **WEB SCRAPING**
````
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
````

#### Stream-lit Deployment
````
import streamlit as st
import pandas as pd
from spellchecker import SpellChecker

df2 = pd.read_csv("C:/Users/Mi/Downloads/Job Analytics/finalcleandata.csv")
df2['Skills1'] = df2['Skills1'].fillna("")
df2["lower_skills1"] = df2['Skills1'].str.lower()
df2["lower_skills2"] = df2['Skills2'].str.lower()
df2["lower_skills3"] = df2['Skills3'].str.lower()
df2["lower_skills4"] = df2['Skills4'].str.lower()
df2["lower_skills5"] = df2['Skills5'].str.lower()
df2["lower_skills6"] = df2['Skills6'].str.lower()
df2["lower_skills7"] = df2['Skills7'].str.lower()


st.set_page_config(
    page_title="Job Analytics",
    page_icon="💼",
    #initial_sidebar_state="collapsed",
)


    
# st.markdown(""" <style>
# #MainMenu {visibility: hidden;}
# </style> """, unsafe_allow_html=True)

# front end elements of the web page 
html_temp = """ 
<div style ="background-color:#3275a8;padding:8px"> 
<h1 style ="font-family:Times New Roman;color:white;text-align:center;">Job Analytics</h1> 
</div> 
"""


# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True)

#st.write("*Our search feature displays the most prevalent experience level, top workplace, and popular classes for a particular skill, along with the total number of jobs related to that skill.*")

st.markdown("<h4> Our search feature displays the most prevalent experience level, top workplace, and popular classes for a particular skill, along with the total number of jobs related to that skill.</h>", unsafe_allow_html=True)



with open('C:/Users/Mi/Downloads/Job Analytics/dictionary.txt') as f:
    skills = f.read().splitlines()

# Create a case-insensitive spell checker
spell = SpellChecker(language=None, case_sensitive=False)
spell.word_frequency.load_words(skills)


text_search = st.text_input("**Search Skills**", value="")

if text_search:
    corrected_input = spell.correction(text_search)
    st.write(f'Searching for jobs related to: {corrected_input}')
    m1 = df2["lower_skills1"].str.contains(corrected_input)
    m2 = df2["lower_skills2"].str.contains(corrected_input)
    m3 = df2["lower_skills3"].str.contains(corrected_input)
    m4 = df2["lower_skills4"].str.contains(corrected_input)
    m5 = df2["lower_skills5"].str.contains(corrected_input)
    m6 = df2["lower_skills6"].str.contains(corrected_input)
    m7 = df2["lower_skills7"].str.contains(corrected_input)


    df_search = df2[m1 | m2 | m3 | m4 | m5 | m6 | m7]
    #.drop('Skills1',axis=1)
    df_search = df_search.reset_index(drop=True)
    df_search.index += 1



    if corrected_input:
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<h4 style="color: black">Most Common Experience Level :</h4>', unsafe_allow_html=True)
            st.markdown('<h4 style="color: black">Most Common Workplace :</h4>', unsafe_allow_html=True)
            st.markdown('<h4 style="color: black">Most Common Classes :</h4>', unsafe_allow_html=True)
            st.markdown('<h4 style="color: black">Total Number of Jobs Available :</h4>', unsafe_allow_html=True)
               
        with col2:
            exp = df_search['Experience Category'].mode()[0]
            st.markdown(f'<h4 style="color: green">{exp}</h4>', unsafe_allow_html=True)
            
            loc = df_search['Locations'].mode()[0]
            st.markdown(f'<h4 style="color: green">{loc}</h4>', unsafe_allow_html=True)
           
            cls = df_search['Cluster'].mode()[0]
            st.markdown(f'<h4 style="color: green">{cls}</h4>', unsafe_allow_html=True)

            num_jobs = str(len(df_search))
            st.markdown(f'<h4 style="color: green">{num_jobs}</h4>', unsafe_allow_html=True)


    
    # if corrected_input:
        # exp = df_search['Experience Category'].mode()[0]
        # st.subheader(f'**Most Common Experience Level** : **:green[{exp}]**')
        
        # loc = df_search['Locations'].mode()[0]
        # st.subheader(f'**Most Common Workplace** : **:green[{loc}]**')
        
        # cls = df_search['Cluster'].mode()[0]
        # st.subheader(f'**Most Common Classes** : **:green[{cls}]**')
    
        # num_jobs = len(df_search)
        # st.subheader(f'**Total Number of Jobs Available** : **:green[{num_jobs}]**')
        
        
# col1, col2, col3, col4, col5 = st.columns(5)

# with col5:
        st.markdown(
            """
            <style>
                .stButton>button {
                    background-color: #3275a8;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Job Details >>"):
            #subprocess.Popen(["streamlit", "run", "job_info.py"])
            
            data = pd.concat([df_search['Company'], df_search['Designation'], df_search['Locations'].rename("Workplace"),df_search['HR_Name'].rename("HR Name"),df_search['Experience'],df_search['Link'].rename("Apply Link")], axis=1)
            st.write(data)
            
            # Define card style
            card_style = """
            <style>
            .card {
                display: inline-block;
                padding: 1rem;
                margin: 1rem;
                background-color: #f0f0f0;
                border-radius: 0.5rem;
                width: 650px;
                height: 310px;
            }
            </style>
            """

            # Add card style to app
            st.markdown(card_style, unsafe_allow_html=True)

            # Loop through records and create cards
            for index, row in data.iterrows():
                card = """
                <div class="card">
                    <h4>Company Name  :  {}</h4>
                    <h5>Designation    :  {}</h5>
                    <h5>Workplace      :  {}</h5>   
                    <h5>HR Name        :  {}</h5>
                    <h5>Experience     :  {}</h5>
                    <a href="{link}">Click Here to Apply</a>
                </div>
                """.format(row['Company'], row['Designation'], row['Workplace'], row['HR Name'], row['Experience'], link=row['Apply Link'])
                
                st.markdown(card, unsafe_allow_html=True)

````

### **LANGUAGES / TOOLS USED**

1. Microsoft Excel
2. Python - Selenium Library
3. SQL - MySQL
4. Microsoft Power BI
5. Sklearn - K Means Clustering Algorithm
6. Streamlit

<br />

### **SNAPSHOTS**

<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/PowerPoint%20Presentation%20-%20Google%20Chrome%2016-05-2023%2000_02_50.png"  width="864" height="470" />

<br />
<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/PowerPoint%20Presentation%20-%20Google%20Chrome%2016-05-2023%2000_03_06.png"  width="864" height="470" />

<br />
<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/PowerPoint%20Presentation%20-%20Google%20Chrome%2016-05-2023%2000_03_19.png"  width="864" height="470" />

<br />
<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/PowerPoint%20Presentation%20-%20Google%20Chrome%2016-05-2023%2000_03_24.png"  width="864" height="470" />

<br />

### **SEARCH BAR INTERFACE**

<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/Job%20Analytics%20%C2%B7%20Streamlit%20-%20Google%20Chrome%2001-05-2023%2000_41_14.png"  width="650" height="500" />

<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/Job%20Analytics%20%C2%B7%20Streamlit%20-%20Google%20Chrome%2016-05-2023%2001_19_59.png"  width="864" height="450" />

<img src ="https://github.com/akashhvyas/Job-Search-Bar/blob/main/Graphic/Job%20Analytics%20%C2%B7%20Streamlit%20-%20Google%20Chrome%2016-05-2023%2001_20_29.png"  width="864" height="470" />

<br />

##### ___CLICK <a href="https://hariharan2608-job-analytics-app-y8xix9.streamlit.app">HERE</a> TO VISIT WEBSITE___

<br />

### CHALLENGES FACED


1. Scraping LinkedIn followers of various companies posed a significant challenge, requiring careful execution
   to avoid being banned.
2. Integrating SpellChecker effectively proved time-consuming and demanding.
3. Following the deployment of the ML model, becoming proficient in HTML and CSS for UI design took considerable time and effort.


<br />

### **CONCLUSION**

1. Software Engineer is most demanding designation in the market.
2. IT jobs are high in demand.
3. There are higher job opportunities for experienced candidates as compared to entry-level freshers.
