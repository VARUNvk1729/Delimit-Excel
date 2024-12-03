import streamlit as st
import pandas as pd

def p(f):
    c = f.getvalue().decode("utf-8").splitlines()
    pths = []
    for l in c:
        if l.strip():
            pths.append(l.strip())
    
    m = 0
    sp = []
    for p in pths:
        s = p.split("\\")
        sp.append(s)
        m = max(m, len(s))

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
    df = df[df.iloc[:, 1:].apply(lambda row: row.str.strip().any(), axis=1)]
    df = df.loc[:, (df != "").any(axis=0)]

    return df

def s(df):
    p = "output.xlsx"
    df.to_excel(p, index=False, engine='openpyxl')
    return p

st.title("FERTIL TASK TEST")
uf = st.file_uploader("Upload a .txt file", type=["txt"])

if uf is not None:
    df = p(uf)
    st.write("Processed DataFrame:")
    df = df.applymap(str)
    st.dataframe(df)
    fp = s(df)
    with open(fp, "rb") as f:
        st.download_button(
            label="Download Excel File",
            data=f,
            file_name="output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
