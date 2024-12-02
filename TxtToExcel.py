import os
import pandas as pd
import streamlit as st
from io import StringIO

st.title("Fertil Test")

uploaded_file = st.file_uploader("Upload file below", type="txt")

if uploaded_file is not None:
    content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    paths = content.strip().split('\n')

    split_data = [path.strip().split(os.sep) for path in paths]
    max_parts = max(len(parts) for parts in split_data)
    for parts in split_data:
        parts.extend([''] * (max_parts - len(parts)))
    dataframe = pd.DataFrame(split_data)

    st.write("Preview")
    st.dataframe(dataframe)

    output_file = "split_file_paths.xlsx"
    dataframe.to_excel(output_file, index=False, header=False)

    with open(output_file, "rb") as file:
        st.download_button(
            label="Download Excel File",
            data=file,
            file_name="split_file_paths.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
