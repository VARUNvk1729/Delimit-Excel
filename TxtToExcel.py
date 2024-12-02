import streamlit as st
import pandas as pd
import os

def process_file(file):
    content = file.getvalue().decode("utf-8").splitlines()
    rows = []
    for line in content:
        if line.strip():
            split_parts = line.split("\\")
            rows.append(split_parts)
    df = pd.DataFrame(rows)
    last_files = []
    for row in rows:
        last_file = ""
        for value in row:
            if '.' in value:
                last_file = value
        last_files.append(last_file)
    df.insert(0, 'Last File', last_files)
    return df

def save_to_excel(df):
    excel_path = "output.xlsx"
    df.to_excel(excel_path, index=False, header=False, engine='openpyxl')
    return excel_path

st.title("File Path Splitter and Extractor")
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    df = process_file(uploaded_file)
    st.write("Processed DataFrame:")
    df = df.applymap(str)  # Convert all data to string type to avoid mixed type warning
    st.dataframe(df)
    excel_file_path = save_to_excel(df)
    with open(excel_file_path, "rb") as f:
        st.download_button(
            label="Download Excel File",
            data=f,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
