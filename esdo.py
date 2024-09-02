import streamlit as st
#import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="ESDO Analytics Report!", page_icon=":bar_chart:",layout="wide")
df = pd.read_csv("report.csv", encoding = "ISO-8859-1")


# Create for Month
month = st.sidebar.multiselect("Select Month", df["Month"].unique())
if not month:
    df1 = df.copy()
else:
    df1 = df[df["Month"].isin(month)]

# Create for Region
region = st.sidebar.multiselect("Select Region", df["Region"].unique())
if not region:
    df2 = df1.copy()
else:
    df2 = df1[df1["Region"].isin(region)]

# Create for Zone
Zone = st.sidebar.multiselect("Select Zone", df2["Zone"].unique())
if not Zone:
    df3 = df2.copy()
else:
    df3 = df2[df2["Zone"].isin(Zone)]

# Create for Area
Area = st.sidebar.multiselect("Select Area",df3["Area"].unique())

# Filter the data based on Region, Zone and Area

if not month and not region and not Zone and not Area:
    filtered_df = df
elif not region and not Zone and not Area:
    filtered_df = df[df["Month"].isin(month)]
elif not Zone and not Area:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not Area:
    filtered_df = df[df["Zone"].isin(Zone)]
elif Zone and Area:
    filtered_df = df3[df["Zone"].isin(Zone) & df3["Area"].isin(Area)]
elif region and Area:
    filtered_df = df3[df["Region"].isin(region) & df3["Area"].isin(Area)]
elif region and Zone:
    filtered_df = df3[df["Region"].isin(region) & df3["Zone"].isin(Zone)]
elif Area:
    filtered_df = df3[df3["Area"].isin(Area)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["Zone"].isin(Zone) & df3["Area"].isin(Area)]


#filtered_df.head()
recoverable = filtered_df['Recoverable'].sum()
recover = filtered_df['Regular'].sum()
otr = recover/recoverable*100
formatted_otr = f"{otr:.2f}"
#otr_avg = filtered_df.groupby(by = ["Recoverable"], as_index = False)["Regular"].sum()

cl1, cl2, cl3 = st.columns((3))
with cl1:
    st.header("Recoverable", divider=True)
    st.subheader(recoverable)
   

with cl2:
    st.header("Recover", divider=True)
    st.subheader(recover)

with cl3:
    st.header("OTR", divider=True)
    st.subheader(formatted_otr)

st.divider()



