from datetime import timedelta

import streamlit as st
from connection import run_sql
from streamlit_extras.chart_container import chart_container

# Query data with 15-minute cache for recent activity
df = run_sql(
    """
with query_history as (
    select
        warehouse_name,
        execution_time,
        bytes_scanned,
    from snowflake.account_usage.query_history
    where start_time >= dateadd('hour', -24, current_timestamp())
    limit 10000
)
select
    warehouse_name,
    count(*) as query_count,
    avg(execution_time) / 1000 as avg_execution_time_s,
    sum(bytes_scanned) / power(1024, 3) as gb_scanned
from query_history
group by warehouse_name
order by query_count desc;
""",
    ttl=timedelta(minutes=15),
)  # More frequent updates for recent activity

st.write(
    "Welcome to your Snowflake monitoring dashboard! Use the navigation to explore different views."
)

# Display overview metrics
st.write("### 24 Hour Activity Overview")
with chart_container(df):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Queries", f"{df['query_count'].sum():,}")

    with col2:
        st.metric("Avg Execution Time", f"{df['avg_execution_time_s'].mean():.1f}s")

    with col3:
        st.metric("Data Scanned", f"{df['gb_scanned'].sum():.1f} GB")

    # Show warehouse activity breakdown
    st.write("### Warehouse Activity")
    st.bar_chart(df, x="warehouse_name", y="query_count", use_container_width=True)

group_by = st.radio(
    "Group by",
    ["minute", "hour", "day"],
    index=1,
    horizontal=True,
)


# Example of longer cache for historical trends
historical_df = run_sql(
    f"""
with query_history as (
    select
        date_trunc('{group_by}', start_time) as {group_by},
        bytes_scanned,
    from snowflake.account_usage.query_history
    where start_time >= dateadd('day', -30, current_timestamp())
    limit 100000
)
select
    {group_by},
    count(*) as query_count,
    sum(bytes_scanned) / power(1024, 4) as tb_scanned
from query_history
group by {group_by}
order by {group_by} asc;
""",
    ttl=timedelta(hours=6),
)  # Longer cache for historical data

st.write("### 30 Day Trends")

st.write("#### Query Volume")
with chart_container(historical_df):
    st.line_chart(historical_df, x=group_by, y="query_count", use_container_width=True)

st.write("#### Data Scanned")
with chart_container(historical_df):
    st.line_chart(historical_df, x=group_by, y="tb_scanned", use_container_width=True)
