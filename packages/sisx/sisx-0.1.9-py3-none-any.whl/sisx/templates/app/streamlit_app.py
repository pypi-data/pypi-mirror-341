import streamlit as st

# Configure page and navigation
st.set_page_config(
    page_title="Snowflake App Dashboard",
    page_icon="❄️",
    layout="wide",
)

# Define pages with material icons
pages = {
    "Monitoring": [
        st.Page("app_pages/home.py", icon=":material/home:", title="Dashboard"),
        st.Page(
            "app_pages/usage_metrics.py",
            icon=":material/query_stats:",
            title="Usage Metrics",
        ),
        st.Page(
            "app_pages/cost_analysis.py",
            icon=":material/payments:",
            title="Cost Analysis",
        ),
    ]
}

# Set up navigation
current_page = st.navigation(pages)

# Display page title with icon
st.title(f"{current_page.icon} {current_page.title}")

# Run the current page
current_page.run()
