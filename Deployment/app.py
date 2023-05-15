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

