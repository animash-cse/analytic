import streamlit as st
#import plotly.express as px
import pandas as pd
import os
import warnings
import statistics 
import altair as alt

#import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

st.set_page_config(page_title="ESDO Analytics Report!", page_icon=":bar_chart:",layout="wide")
df = pd.read_csv("report.csv", encoding = "ISO-8859-1")
#st.title(" :bar_chart: ESDO Analytics Report")
#st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


# fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
# if fl is not None:
    # filename = fl.name
    # st.write(filename)
    # df = pd.read_csv(filename, encoding = "ISO-8859-1") 
# else:
    # os.chdir(r"D:\ESDO-MF\PythonStreamlit-main")
    # df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")
    


# df["Month"] = pd.month_year(df["Month"])

# #Getting the min and max date 
# startDate = pd.month_year(df["Month"]).min()
# endDate = pd.month_year(df["Month"]).max()

# with col1:
    # date1 = pd.month_year(st.date_input("Start Month", startDate))

# with col2:
    # date2 = pd.month_year(st.date_input("End Month", endDate))

# df = df[(df["Month"] >= date1) & (df["Month"] <= date2)].copy()

#st.sidebar.header("Choose your filter: ")

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


col1, col2 = st.columns((2))
shorted_otr = filtered_df.sort_values(by='OTR')
with col1:
    fig = px.bar(shorted_otr, y = "OTR", x = "Branch", text="OTR",hover_data=["Month"], template = "seaborn", title="OTR and Branch")
    st.plotly_chart(fig,use_container_width=True, height = 200)
shorted_recoverable = filtered_df.sort_values(by='Recoverable')
with col2:
    fig = px.bar(shorted_recoverable, x =  "Branch", y = [ "Regular","Recoverable"], text="Month", hover_data=["Recoverable"], title="Recoverable and Recover")
    st.plotly_chart(fig, height = 200)


#     st.subheader("Region wise OTR")
#     fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
#     fig.update_traces(text = filtered_df["Region"], textposition = "outside")
#     st.plotly_chart(fig,use_container_width=True)


#-----------------
#import plotly.express as px

# df = px.data.gapminder().query("continent == 'Oceania'")
# fig = px.bar(df, x='year', y='pop',
#              hover_data=['lifeExp', 'gdpPercap'], color='country',
#              labels={'pop':'population of Canada'}, height=400)
# fig.show()
#--------------------------



# cl1, cl2 = st.columns((2))
# with cl1:
    # with st.expander("Recoverable_ViewData"):
        # st.write(Recoverable_df.style.background_gradient(cmap="Blues"))
        # csv = Recoverable_df.to_csv(index = False).encode('utf-8')
        # st.download_button("Download Data", data = csv, file_name = "Recoverable.csv", mime = "text/csv",
                            # help = 'Click here to download the data as a CSV file')

# with cl2:
    # with st.expander("Region_ViewData"):
        # region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        # st.write(region.style.background_gradient(cmap="Oranges"))
        # csv = region.to_csv(index = False).encode('utf-8')
        # st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        # help = 'Click here to download the data as a CSV file')
        
# filtered_df["month_year"] = filtered_df["Month"].dt.to_period("M")
# st.subheader('Time Series Analysis')

# linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
# fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
# st.plotly_chart(fig2,use_container_width=True)

# with st.expander("View Data of TimeSeries:"):
    # st.write(linechart.T.style.background_gradient(cmap="Blues"))
    # csv = linechart.to_csv(index=False).encode("utf-8")
    # st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

# # Create a treem based on Region, Recoverable, sub-Recoverable
# st.subheader("Hierarchical view of Sales using TreeMap")
# fig3 = px.treemap(filtered_df, path = ["Region","Recoverable","Sub-Recoverable"], values = "Sales",hover_data = ["Sales"],
                  # color = "Sub-Recoverable")
# fig3.update_layout(width = 800, height = 650)
# st.plotly_chart(fig3, use_container_width=True)

# chart1, chart2 = st.columns((2))
# with chart1:
    # st.subheader('Segment wise Sales')
    # fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    # fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    # st.plotly_chart(fig,use_container_width=True)

# with chart2:
    # st.subheader('Recoverable wise Sales')
    # fig = px.pie(filtered_df, values = "Sales", names = "Recoverable", template = "gridon")
    # fig.update_traces(text = filtered_df["Recoverable"], textposition = "inside")
    # st.plotly_chart(fig,use_container_width=True)

# import plotly.figure_factory as ff
# st.subheader(":point_right: Month wise Sub-Recoverable Sales Summary")
# with st.expander("Summary_Table"):
    # df_sample = df[0:5][["Region","Zone","Area","Recoverable","Sales","Profit","Quantity"]]
    # fig = ff.create_table(df_sample, colorscale = "Cividis")
    # st.plotly_chart(fig, use_container_width=True)

    # st.markdown("Month wise sub-Recoverable Table")
    # filtered_df["month"] = filtered_df["Month"].dt.month_name()
    # sub_Recoverable_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Recoverable"],columns = "month")
    # st.write(sub_Recoverable_Year.style.background_gradient(cmap="Blues"))

# # Create a scatter plot
# data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
# data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       # titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       # yaxis = dict(title = "Profit", titlefont = dict(size=19)))
# st.plotly_chart(data1,use_container_width=True)

# with st.expander("View Data"):
    # st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# # Download orginal DataSet
# csv = df.to_csv(index = False).encode('utf-8')
# st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")
