# Install necessary libraries if not already installed
# !pip install pandas streamlit
#https://www.youtube.com/watch?v=4SO3CUWPYf0
#https://genai-asset-tracker.onrender.com/

import pandas as pd
import streamlit as st

# Function to read data from Excel file
def read_data_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        df = pd.DataFrame()
    return df

# Function to save data to Excel file
def save_data_to_excel(data, excel_file):
    data.to_excel(excel_file, index=False)

# Streamlit application
def main():
        
    # Create a sidebar
    with st.sidebar:
        st.sidebar.title("Instructions")
        # Add text to the main page
        st.write('This application will help to Maintain the GenAI assets.')
        st.write('Please select the right option Insert, Update, Delete , Search from the dropdown menu.')
        st.write('Please select the index number correctly Update, Delete .')                   
    st.title('GenAI Asset Management App')
    # Set the background color to black
    st.markdown("""
    <style>
    body {
        background-color: #000;
        color: #fff;
    }
    </style>""", unsafe_allow_html=True)

    excel_file = 'genai_datastore.xlsx'

    df = read_data_from_excel(excel_file)

    if st.checkbox('Show Excel Data'):
        st.write(df)

    operation = st.selectbox('Select Operation', ['Insert', 'Update', 'Delete', 'Search'])

    if operation == 'Insert':
        st.subheader('Insert Data')
        new_data = {}
        for column in df.columns:
            new_value = st.text_input(f'Enter value for {column}', key=column)
            new_data[column] = new_value
        if st.button('Insert Data'):
            df = df.append(new_data, ignore_index=True)
            save_data_to_excel(df, excel_file)
            st.success('Data inserted successfully!')

    elif operation == 'Update':
        st.subheader('Update Data')
        row_index = st.number_input('Enter row index to update', min_value=0, max_value=len(df)-1)
        if row_index is not None:
            updated_data = {}
            for column in df.columns:
                updated_value = st.text_input(f'Enter new value for {column}', key=column)
                updated_data[column] = updated_value
            if st.button('Update Data'):
                df.loc[row_index] = updated_data
                save_data_to_excel(df, excel_file)
                st.success('Data updated successfully!')

    elif operation == 'Delete':
        st.subheader('Delete Data')
        delete_index = st.number_input('Enter row index to delete', min_value=0, max_value=len(df)-1)
        if st.button('Delete Data'):
            df.drop(delete_index, inplace=True)
            save_data_to_excel(df, excel_file)
            st.success('Data deleted successfully!')

    elif operation == 'Search':
        st.subheader('Search Data')
        search_term = st.text_input('Enter search term:')
        if st.button('Search'):
            print("Search Term:",search_term)
            df = pd.read_excel(excel_file)
            search_results = df[df.apply(lambda row: any(search_term.lower() in str(cell).lower() for cell in row), axis=1)]
            st.write(search_results)

if __name__ == '__main__':
    main()