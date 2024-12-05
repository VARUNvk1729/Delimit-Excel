# import streamlit as st
# import pandas as pd

# def p(f):
#     c = f.getvalue().decode("utf-8").splitlines()
#     pths = []
#     for l in c:
#         if l.strip():
#             pths.append(l.strip())
    
#     m = 0
#     sp = []
#     for p in pths:
#         s = p.split("\\")
#         sp.append(s)
#         m = max(m, len(s))

#     h = ["Drive"] + [f"Folder Level {i}" for i in range(m - 1)] + ["File Name"]
    
#     d = []
#     for p in sp:
#         r = [""] * m
#         for i, part in enumerate(p):
#             if "." not in part:
#                 r[i] = part
#         fn = p[-1] if "." in p[-1] else ""
#         r.append(fn)
#         d.append(r)
    
#     df = pd.DataFrame(d, columns=h)
#     df = df[df.iloc[:, 1:].apply(lambda row: row.str.strip().any(), axis=1)]
#     df = df.loc[:, (df != "").any(axis=0)]

#     return df

# def s(df):
#     p = "output.xlsx"
#     df.to_excel(p, index=False, engine='openpyxl')
#     return p

# st.title("FERTIL TASK TEST")
# uf = st.file_uploader("Upload a .txt file", type=["txt"])

# if uf is not None:
#     df = p(uf)
#     st.write("Processed DataFrame:")
#     df = df.applymap(str)
#     st.dataframe(df)
#     fp = s(df)
#     with open(fp, "rb") as f:
#         st.download_button(
#             label="Download Excel File",
#             data=f,
#             file_name="output.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )


#VERSION -2 AFTER CHANGES

import streamlit as st
import pandas as pd
import re

def p(f):
    c = f.getvalue().decode("utf-8").splitlines()
    pths = [l.strip() for l in c if l.strip()]
    m = 0
    sp = [p.split("\\") for p in pths]
    m = max(len(s) for s in sp)
    h = ["Drive"] + [f"Folder Level {i}" for i in range(m - 1)] + ["File Name"]
    d = []
    for p in sp:
        r = [""] * m
        for i, part in enumerate(p):
            if "." not in part:
                r[i] = part
        fn = p[-1] if "." in p[-1] else ""
        r.append(fn)
        d.append(r)
    df = pd.DataFrame(d, columns=h)
    folder_column = next((col for col in df.columns if df[col].apply(lambda x: bool(re.match(r"\d{4}-\s", str(x)))).any()), None)
    if folder_column:
        df.insert(df.columns.get_loc(folder_column) + 1, f"Folder Level {len(df.columns) - 1}", df[folder_column].apply(
            lambda x: re.match(r"(\d{4})-", str(x)).group(1) if re.match(r"(\d{4})-", str(x)) else ""
        ))
        df.insert(df.columns.get_loc(folder_column) + 2, f"Folder Level {len(df.columns)}", df[folder_column].apply(
            lambda x: re.match(r"\d{4}-\s(.+)", str(x)).group(1) if re.match(r"\d{4}-\s(.+)", str(x)) else ""
        ))
    df = df[df.iloc[:, 1:].apply(lambda row: row.str.strip().any(), axis=1)]
    df = df.loc[:, (df != "").any(axis=0)]
    sequential_headers = ["Drive"] + [f"Folder Level {i}" for i in range(0, len(df.columns) - 2)] + ["File Name"]
    df.columns = sequential_headers
    return df

def s(df):
    p = "output.xlsx"
    df.to_excel(p, index=False, engine='openpyxl')
    return p

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .stTitle {
        font-size: 2.5rem !important;
        padding-bottom: 2rem;
    }
    .section-divider {
        margin: 2rem 0;
        text-align: center;
        border-top: 3px solid #5e81ac;
    }
    .header-container {
        background-color: #e9eff5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-container h2 {
        color: #5e81ac;
        font-weight: bold;
    }
    .stDataFrame {
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f9fafb;
    }
    .stButton>button {
        background-color: #88c0d0;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #5e81ac;
    }
    .stFileUploader {
        background-color: #f0f4f8;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>FERTIL TASK TEST</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    st.header("Full Data")
    st.markdown("</div>", unsafe_allow_html=True)
    
    uf1 = st.file_uploader("Upload a .txt file (Full Data)", type=["txt"])
    if uf1 is not None:
        with st.spinner('Processing full data...'):
            df_full = p(uf1)
            st.success('Full data processed successfully!')
            st.write("Processed DataFrame (Full Data):")
            df_full = df_full.applymap(str)
            st.dataframe(df_full, use_container_width=True)
            
            fp1 = s(df_full)
            with open(fp1, "rb") as f:
                st.download_button(
                    label="📥 Download Full Data as Excel",
                    data=f,
                    file_name="full_data_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    st.header("Filtered Data")
    st.markdown("</div>", unsafe_allow_html=True)
    
    uf2 = st.file_uploader("Upload a .txt file (Filtered Data)", type=["txt"])
    if uf2 is not None:
        with st.spinner('Processing filtered data...'):
            df_filtered = p(uf2)
            df_filtered = df_filtered[df_filtered["File Name"].str.strip() != ""]
            df_filtered = df_filtered.loc[:, (df_filtered != "").any(axis=0)]
            current_cols = df_filtered.columns.tolist()
            new_cols = ["Drive"]
            folder_levels = [col for col in current_cols if col.startswith("Folder Level")]
            new_cols.extend([f"Folder Level {i}" for i in range(len(folder_levels))])
            new_cols.append("File Name")
            df_filtered.columns = new_cols
            
            st.success('Filtered data processed successfully!')
            st.write("Processed DataFrame (Filtered Data):")
            df_filtered = df_filtered.applymap(str)
            st.dataframe(df_filtered, use_container_width=True)
            
            fp2 = s(df_filtered)
            with open(fp2, "rb") as f:
                st.download_button(
                    label="📥 Download Filtered Data as Excel",
                    data=f,
                    file_name="filtered_data_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
