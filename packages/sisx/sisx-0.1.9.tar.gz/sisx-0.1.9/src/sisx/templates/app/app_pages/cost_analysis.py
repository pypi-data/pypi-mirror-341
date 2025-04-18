from datetime import timedelta

import streamlit as st
from connection import run_sql
from streamlit_extras.chart_container import chart_container

# Query data with 1-hour cache for cost metrics
df = run_sql(
    """
with warehouse_metering_history as (
    select
        to_varchar(start_time::date, 'YYYY-MM-DD') as usage_date,
        warehouse_name,
        credits_used,
    from snowflake.account_usage.warehouse_metering_history
    where start_time >= dateadd('day', -7, current_timestamp())
    limit 10000
)
select
    usage_date,
    warehouse_name,
    sum(credits_used) as credits_used,
from warehouse_metering_history
group by usage_date, warehouse_name
order by usage_date asc, warehouse_name asc;
""",
    ttl=timedelta(hours=1),
)  # Cost data updates less frequently

st.write("Monitor your Snowflake credit usage and costs across warehouses.")

# Pivot the data for better visualization
df_pivot = df.pivot(
    index="usage_date", columns="warehouse_name", values="credits_used"
).fillna(0)

# Display metrics using chart container
with chart_container(df):
    # Show stacked bar chart of credits by warehouse
    st.bar_chart(df_pivot, use_container_width=True)
    st.caption("Daily Credits Used by Warehouse")

    # Show metrics
    total_credits = df["credits_used"].sum()
    total_queries = df["query_count"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Credits Used", f"{total_credits:.1f}")
    with col2:
        st.metric("Total Queries Run", f"{total_queries:,}")

    # Show detailed table with chart container
    st.write("### Daily Warehouse Usage Details")
    st.dataframe(
        df.pivot_table(
            index="warehouse_name",
            values=["credits_used", "query_count"],
            aggfunc="sum",
        )
        .round(2)
        .sort_values(by="credits_used", ascending=False),
        use_container_width=True,
    )
