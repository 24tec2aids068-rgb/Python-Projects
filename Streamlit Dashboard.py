import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Streamlit Interactive Dashboard")

st.sidebar.header("🔍 Filters")

report_type = st.sidebar.selectbox(
    "Select Data Type",
    ["Sales", "Users", "Products"]
)

value_range = st.sidebar.slider(
    "Select Value Range",
    1, 100, (20, 70)
)

np.random.seed(1)
data = pd.DataFrame({
    "Category": ["A", "B", "C", "D"] * 25,
    "Value": np.random.randint(10, 100, 100),
    "Index": range(1, 101)
})

filtered = data[
    (data["Value"] >= value_range[0]) &
    (data["Value"] <= value_range[1])
]

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(data))
col2.metric("Filtered Records", len(filtered))
col3.metric("Average Value", round(filtered["Value"].mean(), 2))

st.markdown("---")

left, right = st.columns(2)

with left:
    st.subheader("📈 Bar Chart")
    bar_fig = px.bar(filtered, x="Category", y="Value", color="Category")
    st.plotly_chart(bar_fig, use_container_width=True)

with right:
    st.subheader(" Line Chart")
    line_fig = px.line(filtered, x="Index", y="Value")
    st.plotly_chart(line_fig, use_container_width=True)


st.subheader("Filtered Data Table")
st.dataframe(filtered, use_container_width=True)

st.markdown("---")
st.markdown("✔ Built using **Streamlit** | Made with ")

