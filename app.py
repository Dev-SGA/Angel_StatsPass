import streamlit as st
import pandas as pd

# Page configuration for a professional look
st.set_page_config(page_title="Angel Performance Dashboard", layout="wide")

# Custom CSS to refine the interface
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
    }
    .main {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Data Structure (Cleaned version without active windows)
data = {
    "Match": ["IMG", "Orlando", "Weston", "South Florida"],
    "Minutes Played (Text)": ["40:00", "40:00", "58:20", "19:00"],
    "Total Minutes": [40, 40, 58.33, 19],
    "Total Passes": [10, 30, 24, 11],
    "Passes per 90 min": [22.5, 67.5, 37.0, 52.1],
    "Active Minutes": [8, 21, 21, 10],
    "% Participation": [20.0, 52.5, 36.2, 52.6]
}

df = pd.DataFrame(data)

# --- SIDEBAR / FILTERS ---
st.sidebar.title("📊 Analysis Filters")
match_option = st.sidebar.selectbox("Select Match:", ["General"] + list(df["Match"].unique()))

# --- MAIN TITLE ---
st.title("⚽ Performance Dashboard: Angel")
st.markdown(f"**Viewing:** {match_option}")
st.divider()

# --- FILTER LOGIC & AVERAGE CALCULATIONS ---
if match_option == "General":
    display_df = df
    avg_p90 = df["Passes per 90 min"].mean()
    total_passes = df["Total de Passes"].sum() if "Total de Passes" in df else df["Total Passes"].sum()
    avg_participation = df["% Participation"].mean()
    title_suffix = "Overall Averages"
else:
    display_df = df[df["Match"] == match_option]
    avg_p90 = display_df["Passes per 90 min"].iloc[0]
    total_passes = display_df["Total Passes"].iloc[0]
    avg_participation = display_df["% Participation"].iloc[0]
    title_suffix = f"Stats: {match_option}"

# --- SECTION 1: KEY PERFORMANCE INDICATORS (KPIs) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Volume (Passes/90min)", value=f"{avg_p90:.1f}")

with col2:
    st.metric(label="Total Passes", value=total_passes)

with col3:
    st.metric(label="Participation Density", value=f"{avg_participation:.1f}%")

st.divider()

# --- SECTION 2: TABLES AND CHARTS ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader(f"📋 {title_suffix}")
    
    # Table display with progress bars and English headers
    st.dataframe(
        display_df[["Match", "Minutes Played (Text)", "Total Passes", "Passes per 90 min", "% Participation"]],
        column_config={
            "Match": st.column_config.TextColumn("Match"),
            "Minutes Played (Text)": st.column_config.TextColumn("Time on Pitch"),
            "Total Passes": st.column_config.NumberColumn("Passes", format="%d 🎯"),
            "Passes per 90 min": st.column_config.NumberColumn("P/90", format="%.1f"),
            "% Participation": st.column_config.ProgressColumn(
                "Density %", 
                help="Percentage of minutes where the player was involved in a pass", 
                format="%.1f%%", 
                min_value=0, 
                max_value=100
            ),
        },
        hide_index=True,
        use_container_width=True
    )

with col_right:
    st.subheader("📈 Volume Comparison")
    # Bar chart comparing Passes/90min across matches
    st.bar_chart(df.set_index("Match")["Passes per 90 min"], color="#1f77b4")

# --- SECTION 3: MINUTAGE SUMMARY ---
st.subheader("⏱️ Active Minutes per Match")
cols = st.columns(len(display_df))

for i, row in display_df.iterrows():
    with cols[i % len(display_df)]:
        # Info cards for each selected match
        st.info(f"**{row['Match']}**\n\nActive in **{row['Active Minutes']}** out of **{row['Total Minutes']}** min.")

st.markdown("---")
st.caption("Data processed based on official scouting logs.")
