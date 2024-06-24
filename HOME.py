import streamlit as st
import pandas as pd

# Load the tasks.csv file
tasks_file = 'app_data/tasks.csv'
tasks_df = pd.read_csv(tasks_file)

# Get the unique areas and capitalize them
unique_areas = sorted(tasks_df['area'].unique())
unique_areas = [area.capitalize() for area in unique_areas]

st.set_page_config(
    page_title="AI Task and Evaluation Explorer",
    page_icon="🏠",
    layout="wide",
)

def home():
    st.title('Welcome to the SOTA Explorer.')
    st.write('This application provides a nested directory of over 1,000 ML tasks, classified by domain.')
    st.write('Please choose a domain from the sidebar on the left to find information about thousands of SOTA models, '
             'and their performance on popular ML benchmarks.')
    st.write('Acknowledgement is given to the Paperswithcode team for allowing me to put this application '
             'together with their wonderful API client')

home()
