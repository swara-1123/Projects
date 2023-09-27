import streamlit as st
import pandas as pd
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go

st.header(":blue[Relation Between Laptop Price and Features]")

#resourses path
FILE_DIR1 = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = os.path.join(FILE_DIR1,os.pardir)
dir_of_interest = os.path.join(FILE_DIR, "resourses")
DATA_PATH = os.path.join(dir_of_interest, "data")

#Load data
DATA_PATH1=os.path.join(DATA_PATH, "laptop_price.csv")
df=pd.read_csv(DATA_PATH1)
data=df.copy()
data.drop("MRP", axis=1, inplace=True)


feature=st.selectbox(
    "Select Feature to See the Relation",
    (data.columns))

#Create relationship Bar plot for min max and average MRP for selected feature
aggregate=df.groupby(feature).agg({"MRP":{"min", "max", "mean"}})
aggregate.columns= ["_".join(col) for col in aggregate.columns]
aggregate= aggregate.reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=aggregate[feature],
                         y=aggregate["MRP_min"],
                         name="Minimum Price",
                         mode="markers",
                         showlegend=True,
                         marker=dict(color="red", size=8)))

fig.add_trace(go.Scatter(x=aggregate[feature],
                         y=aggregate["MRP_mean"],
                         name="Average Price",
                         mode="markers",
                         showlegend=True,
                         marker=dict(color="green",size=15)))

fig.add_trace(go.Scatter(x=aggregate[feature],
                         y=aggregate["MRP_max"],
                         name="Maximum Price",
                         mode="markers",
                         showlegend=True,
                         marker=dict(color="blue",size=20)))
#Add vertical line to differentiate category
for i, row in aggregate.iterrows():
    if row["MRP_min"]!=row["MRP_max"]:
        fig.add_shape(
            dict(type="line",
                 x0=row[feature],
                 x1=row[feature],
                 y0=row["MRP_min"],
                 y1=row["MRP_max"],
                 line=dict(color="pink",width=0.5)))
fig.update_layout(title="Average, Minimum and Maximum Laptop Price by {}".format(feature))
st.plotly_chart(fig, use_container_width=True)