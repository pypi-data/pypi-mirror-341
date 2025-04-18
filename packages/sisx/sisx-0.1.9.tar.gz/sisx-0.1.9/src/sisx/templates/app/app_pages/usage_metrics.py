from datetime import timedelta

import streamlit as st
from connection import get_table, run_snowpark
from snowflake.snowpark.functions import (
    avg,
    col,
    count,
    current_timestamp,
    date_trunc,
    dateadd,
    lit,
    sum,
)
from streamlit_extras.chart_container import chart_container

group_by = st.radio(
    "Group by",
    ["minute", "hour", "day"],
    index=1,
    horizontal=True,
)

query_history = (
    get_table("snowflake.account_usage.query_history")
    .select(
        date_trunc(group_by, col("start_time")).alias(group_by),
        "execution_time",
        "bytes_scanned",
    )
    .where(col("start_time") >= dateadd("hour", lit(-24), current_timestamp()))
    .limit(100_000)
)

df = query_history.group_by(group_by).agg(
    count(col("execution_time")).alias("query_count"),
    avg(col("execution_time") / 1000).alias("avg_execution_time_s"),
    sum(col("bytes_scanned") / pow(1024, 3)).alias("gb_scanned"),
)

# Query data with 30-minute cache for weekly metrics
pd_df = run_snowpark(df, ttl=timedelta(minutes=30))

st.write("Track your Snowflake query performance and resource utilization over time.")

# Display metrics using chart container
with chart_container(pd_df):
    col1, col2 = st.columns(2)

    with col1:
        st.line_chart(pd_df, x=group_by, y="query_count", use_container_width=True)
        st.caption("Daily Query Count")

    with col2:
        st.line_chart(
            pd_df, x=group_by, y="avg_execution_time_s", use_container_width=True
        )
        st.caption("Average Execution Time (seconds)")

    st.area_chart(pd_df, x=group_by, y="gb_scanned", use_container_width=True)
    st.caption("Data Scanned (GB)")
