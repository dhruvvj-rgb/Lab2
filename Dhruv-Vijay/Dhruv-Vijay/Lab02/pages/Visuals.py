# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
infile = open("data.json")
data = json.load(infile)
infile.close()

hobby_data = pd.DataFrame(data["data_points"])

st.header(data["chart_title"])

st.subheader("Static Bar Chart")
st.bar_chart(
    hobby_data,
    x="label",
    y="value",
    x_label="Hobby",
    y_label="Minutes per Week"
)

st.subheader("Dynamic Pie Chart")

if "minimum_minutes" not in st.session_state:
    st.session_state["minimum_minutes"] = 0

st.slider(
    "Minimum weekly minutes to include",
    min_value=0,
    max_value=60,
    step=5,
    key="minimum_minutes"
)

filtered_data = hobby_data[
    hobby_data["value"] >= st.session_state["minimum_minutes"]
]

pie_chart = alt.Chart(filtered_data).mark_arc().encode(
    theta=alt.Theta("value:Q", title="Minutes per Week"),
    color=alt.Color("label:N", title="Hobby"),
    tooltip=[
        alt.Tooltip("label:N", title="Hobby"),
        alt.Tooltip("value:Q", title="Minutes per Week")
    ]
).properties(
    title="Hobby Time Distribution"
)

st.altair_chart(pie_chart, use_container_width=True)


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

st.header("Survey Data Visualizations")

csv_data = pd.read_csv("data.csv")

if csv_data.empty:
    st.warning("Submit some survey responses before viewing the CSV visualizations.")
else:
    csv_data["Value"] = pd.to_numeric(csv_data["Value"], errors="coerce")
    csv_data = csv_data.dropna(subset=["Value"])

    if csv_data.empty:
        st.warning("The CSV does not contain any numeric values yet.")
    else:
        average_data = csv_data.groupby("Category", as_index=False)["Value"].mean()

        st.subheader("Static Bar Chart: Average Weekly Minutes by Hobby")
        st.bar_chart(
            average_data,
            x="Category",
            y="Value",
            x_label="Hobby",
            y_label="Average Minutes per Week"
        )

        st.subheader("Dynamic Scatter Plot: Survey Responses")

        if "csv_minimum_minutes" not in st.session_state:
            st.session_state["csv_minimum_minutes"] = 0

        max_minutes = max(10, int(csv_data["Value"].max()))

        if st.session_state["csv_minimum_minutes"] > max_minutes:
            st.session_state["csv_minimum_minutes"] = 0

        st.slider(
            "Minimum survey minutes to include",
            min_value=0,
            max_value=max_minutes,
            step=5,
            key="csv_minimum_minutes"
        )

        filtered_csv = csv_data[
            csv_data["Value"] >= st.session_state["csv_minimum_minutes"]
        ]

        scatter_chart = alt.Chart(filtered_csv).mark_circle(size=120).encode(
            x=alt.X("Category:N", title="Hobby"),
            y=alt.Y("Value:Q", title="Minutes per Week"),
            tooltip=[
                alt.Tooltip("Category:N", title="Hobby"),
                alt.Tooltip("Value:Q", title="Minutes per Week")
            ]
        ).properties(
            title="Survey Responses Meeting the Minimum"
        )

        st.altair_chart(scatter_chart, use_container_width=True)
