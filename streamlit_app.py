#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency
from PIL import Image

def filterBy(df, campus):
    if campus=='All':
        return df
    else:  
        filtered_df = df[df['Campus'] == campus]  
        return filtered_df

def loadcsvfile(campus):
    csvfile = 'Employability-2017.csv'
    df = pd.read_csv(csvfile, dtype='str', header=0, sep = ",", encoding='latin') 
    return df

def createPlots(df, columnName):
    st.write('Graduate Distribution by ' + columnName)
    scounts=df[columnName].value_counts()
    labels = list(scounts.index)
    sizes = list(scounts.values)
    custom_colours = ['#ff7675', '#74b9ff']
    fig = plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels = labels, textprops={'fontsize': 10}, startangle=140, autopct='%1.0f%%', colors=custom_colours)
    plt.subplot(1, 2, 2)
    sns.barplot(x = scounts.index, y = scounts.values, palette= 'viridis')
    st.pyplot(fig)

    # get value counts and percentages of unique values in column 
    value_counts = df[columnName].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df[columnName].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    st.write(pd.DataFrame(result))
    
    return

def createTable(df, columnName):  
    st.write('Graduate Distribution by ' + columnName)
    # get value counts and percentages of unique values in column 
    value_counts = df[columnName].value_counts(normalize=True)
    value_counts = value_counts.mul(100).round(2).astype(str) + '%'
    value_counts.name = 'Percentage'

    # combine counts and percentages into a dataframe
    result = pd.concat([df[columnName].value_counts(), value_counts], axis=1)
    result.columns = ['Counts', 'Percentage']
    st.write(pd.DataFrame(result))
    
    return

def twowayPlot(df, var1, var2):
    fig = plt.figure(figsize =(10, 3))
    p = sns.countplot(x=var1, data = df, hue=var2, palette='bright')
    _ = plt.setp(p.get_xticklabels(), rotation=90) 
    st.pyplot(fig)

# Define the Streamlit app
def app():
    st.title("Welcome to the WVSU Employability Report 2017")      
    st.subheader("(c) 2023 WVSU Management Information System")
                 
    st.write("This dashboard is managed by: Dr. Wilhelm P. Cerbo \nDirector, University Planning Office, updo@wvsu.edu.ph")
                 
    st.write("The employability of university graduates can vary depending on a variety of factors, such as their field of study, their level of academic achievement, their relevant work experience, their soft skills, and the current state of the job market.")

    #create a dataframe
    df = pd.DataFrame()
    
    st.subheader("Graduate Employability")
    campus = 'Main'
    options = ['All', 'Main Campus', 'CAF Campus', 'Calinog Campus', 'Janiuay Campus', 'Lambunao Campus', 'Pototan Campus']
    
    selected_option = st.selectbox('Select the campus', options)
    if selected_option=='All':
        campus = selected_option
        df = loadcsvfile(campus)
    else:
        campus = selected_option
        df = loadcsvfile(campus)
        df = filterBy(df, campus)
        
    if st.button('Distribution By Course'):
        df = filterBy(df, campus)
        createPlots(df, 'Course')

    if st.button('Distribution By College'):
        df = filterBy(df, campus)  
        createPlots(df, 'College')
    
    if st.button('Distribution By Campus'):
        df = filterBy(df, campus)  
        createPlots(df, 'Campus')
        
    if st.button('Distribution By Employment Status'):
        df = filterBy(df, campus)  
        createPlots(df, 'Status')
    
    if st.button('Distribution By Status across Course'):
        df = filterBy(df, campus)  
        twowayPlot(df, 'Course', 'Status')
        
    if st.button('Distribution By Status across Colleges'):
        df = filterBy(df, campus)  
        twowayPlot(df, 'College', 'Status')
        
    if st.button('Distribution By Status across Campuses'):
        df = filterBy(df, campus)  
        twowayPlot(df, 'Campus', 'Status')
        
#run the app
if __name__ == "__main__":
    app()
