import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ------------------------------
# Page Configuration & Custom CSS
# ------------------------------
st.set_page_config(
    page_title="City Carbon Footprint Tracker + Citizen Rewards",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern look
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf, #2e7bcf);
        color: white;
    }
    .stButton>button {
        background-color: #2e7bcf;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2e7bcf;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Emission Factors (kg CO₂/km)
# ------------------------------
EMISSION_FACTORS = {
    "Car": 0.25,
    "Bus": 0.10,
    "Train": 0.06,   # Typical value for intercity trains
    "Subway": 0.05,  # Urban rail systems are very energy efficient
    "Bicycle": 0.0,
    "Walking": 0.0
}

ELECTRICITY_CO2_PER_KWH = 0.42  # Electricity emissions per kWh (NJ grid)

# ------------------------------
# Average Daily Emission for NJ (per capita)
# ------------------------------
# Based on research, the NJ per capita daily CO₂ emission is roughly 25 kg CO₂ per day.
NJ_AVG_EMISSION = 25.0  # kg CO₂ per day

# ------------------------------
# Total Emissions for New Jersey (simulated data)
# ------------------------------
NJ_TOTAL_EMISSIONS_MT = 80e6   # 80 million metric tons CO₂

# File to store user points (CSV format)
USER_POINTS_FILE = "user_points.txt"

def main():
    st.title("City Carbon Footprint Tracker + Citizen Rewards System")
    st.subheader("Serving New Jersey (NJ)")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Select Page", [
        "Personal Carbon Calculator",
        "NJ Overview",
        "Leaderboard"
    ])

    if menu == "Personal Carbon Calculator":
        personal_calculator()
    elif menu == "NJ Overview":
        nj_overview()
    elif menu == "Leaderboard":
        leaderboard()

def personal_calculator():
    """Interactive calculator for individual carbon emissions with reward points update."""
    st.header("Personal Carbon Footprint Calculator")
    st.write(
        f"Enter your daily commute and electricity usage to calculate your carbon emissions and earn reward points. "
        f"Tip: The NJ average daily CO₂ emission is about {NJ_AVG_EMISSION} kg. Lower your emissions to earn points!"
    )

    # Username input
    username = st.text_input("Enter your username", value="")

    # Input for transportation and electricity usage
    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox("Transportation Mode", list(EMISSION_FACTORS.keys()))
        distance = st.number_input("Travel Distance (km)", min_value=0.0, value=0.0, step=0.1)
    with col2:
        electricity_usage = st.number_input("Daily Electricity Usage (kWh)", min_value=0.0, value=0.0, step=0.1)

    # Calculate emissions
    transport_emission = distance * EMISSION_FACTORS[mode]
    electricity_emission = electricity_usage * ELECTRICITY_CO2_PER_KWH
    total_emission = transport_emission + electricity_emission

    # Display emissions
    st.subheader("Your Daily Carbon Emissions")
    st.write(f"**Transport Emissions:** {transport_emission:.2f} kg CO₂")
    st.write(f"**Electricity Emissions:** {electricity_emission:.2f} kg CO₂")
    st.write(f"**Total Emissions:** {total_emission:.2f} kg CO₂")

    # Reward points calculation using NJ average daily emission:
    # For each 1 kg below NJ average, earn 0.5 points; for each 1 kg above, lose 0.5 points.
    daily_points = calculate_reward_points(total_emission)
    st.subheader("Reward Points")
    st.write(f"Points earned today: **{daily_points:.2f} points**")
    st.info("Reduce your emissions below the NJ per capita average to earn more points!")

    # Display a progress bar gauge if user earns positive points
    if daily_points > 0:
        # Target points set to 10 for full gauge (i.e., if user is 10 points ahead, gauge is full)
        progress_ratio = min(1.0, daily_points / 10.0)
        st.progress(progress_ratio)
    else:
        st.warning("Your emissions are above the NJ average. Try to reduce them to earn points!")

    # Emission Reduction Tips (interactive)
    if st.checkbox("Show Emission Reduction Tips"):
        st.markdown("""
        **Tips to reduce your carbon footprint:**
        - Use public transportation, biking, or walking whenever possible.
        - Conserve electricity by turning off unused devices.
        - Consider carpooling or telecommuting.
        - Reduce, reuse, and recycle.
        """)

    # Update user points file if username is provided
    if username.strip() != "":
        update_user_points(username.strip(), daily_points)

    # Simulate a 7-day emission trend chart (random values for illustration)
    st.subheader("Your Emission Trend (Past 7 Days)")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
    simulated_emissions = np.linspace(total_emission * 1.1, total_emission * 0.9, 7) + np.random.normal(0, 0.5, 7)
    df_trend = pd.DataFrame({
        "Date": dates,
        "Emissions (kg CO₂)": simulated_emissions
    })
    fig_trend = px.line(df_trend, x="Date", y="Emissions (kg CO₂)", markers=True,
                        title="Your Emission Trend (Past 7 Days)")
    st.plotly_chart(fig_trend)

def calculate_reward_points(total_emission: float) -> float:
    """
    Calculate reward points based on total daily emissions and the NJ per capita average.
    For each 1 kg below the NJ average, earn 0.5 points;
    for each 1 kg above the NJ average, lose 0.5 points.
    """
    return (NJ_AVG_EMISSION - total_emission) * 0.5

def update_user_points(username: str, daily_points: float):
    """
    Update the user's cumulative points stored in a text file.
    The file is in CSV format with columns: username, cumulative_points, yesterday_points.
    If the user exists, set yesterday_points to the old cumulative_points and add daily_points to cumulative_points.
    If not, add a new record with cumulative_points = daily_points and yesterday_points = 0.
    """
    if os.path.exists(USER_POINTS_FILE):
        df = pd.read_csv(USER_POINTS_FILE)
    else:
        df = pd.DataFrame(columns=["username", "cumulative_points", "yesterday_points"])

    if username in df["username"].values:
        idx = df.index[df["username"] == username][0]
        old_points = df.at[idx, "cumulative_points"]
        df.at[idx, "yesterday_points"] = old_points
        df.at[idx, "cumulative_points"] = old_points + daily_points
    else:
        new_row = {"username": username, "cumulative_points": daily_points, "yesterday_points": 0.0}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(USER_POINTS_FILE, index=False)
    st.success(f"User '{username}' points updated.")

def nj_overview():
    """Overview of New Jersey state-level carbon emissions with a detailed NJ-only map."""
    st.header("New Jersey State Overview")
    st.write("Simulated heatmap of county-level carbon emissions across New Jersey.")
    st.write(f"**Total CO₂ Emissions for New Jersey:** {NJ_TOTAL_EMISSIONS_MT / 1e6:.1f} million metric tons")

    # Interactive slider to filter counties by minimum emission value (in million tons)
    min_emission = st.slider("Filter counties by minimum emission (million tons):", min_value=0, max_value=20, value=0)

    # Detailed NJ counties (21 counties) with approximate center coordinates
    county_data = pd.DataFrame({
        "County": [
            "Atlantic", "Bergen", "Burlington", "Camden", "Cape May", "Cumberland", "Essex",
            "Gloucester", "Hudson", "Hunterdon", "Mercer", "Middlesex", "Monmouth", "Morris",
            "Ocean", "Passaic", "Salem", "Somerset", "Sussex", "Union", "Warren"
        ],
        "lat": [
            39.533, 40.912, 39.883, 39.925, 38.935, 39.410, 40.750,
            39.710, 40.730, 40.550, 40.220, 40.500, 40.200, 40.800,
            39.950, 41.000, 39.600, 40.550, 41.000, 40.650, 40.700
        ],
        "lon": [
            -74.616, -74.134, -74.909, -75.119, -74.906, -75.001, -74.200,
            -75.107, -74.010, -74.983, -74.766, -74.450, -74.000, -74.500,
            -74.300, -74.100, -75.300, -74.600, -74.700, -74.300, -75.000
        ],
        # Simulated emissions in million tons (for illustration)
        "Emissions": [
            8, 12, 10, 11, 7, 9, 15, 13, 14, 8, 10, 11, 9, 12, 7, 10, 6, 9, 8, 10, 7
        ]
    })

    # Apply filter based on the slider selection
    filtered_data = county_data[county_data["Emissions"] >= min_emission]

    st.subheader("County-Level Emissions Heatmap (Detailed NJ)")
    fig = px.scatter_mapbox(
        filtered_data,
        lat="lat",
        lon="lon",
        size="Emissions",
        color="Emissions",
        hover_name="County",
        hover_data={"Emissions": True, "lat": False, "lon": False},
        zoom=7.5,  # Adjust zoom for a NJ-only view
        height=600,
        title="New Jersey County Emission Indicators"
    )
    # Center the map on New Jersey
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 40.0583, "lon": -74.4057},
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )
    st.plotly_chart(fig)

def leaderboard():
    """Display the leaderboard with ranking, ranking changes, and a search function."""
    st.header("Points Leaderboard")
    st.write("Below is the leaderboard showing all users ranked based on cumulative eco-points.")

    # Load user points file
    if os.path.exists(USER_POINTS_FILE):
        df = pd.read_csv(USER_POINTS_FILE)
    else:
        st.write("No user data available yet.")
        return

    # Today's ranking based on cumulative_points (descending order)
    df_sorted = df.sort_values(by="cumulative_points", ascending=False).reset_index(drop=True)
    df_sorted["Rank"] = df_sorted.index + 1

    # Yesterday's ranking based on yesterday_points (descending order)
    df_sorted_yesterday = df.sort_values(by="yesterday_points", ascending=False).reset_index(drop=True)
    df_sorted_yesterday["Yesterday_Rank"] = df_sorted_yesterday.index + 1

    # Merge yesterday's ranking into today's ranking based on username
    df_merged = pd.merge(df_sorted, df_sorted_yesterday[["username", "Yesterday_Rank"]], on="username", how="left")
    # Calculate ranking change (positive means improved ranking compared to yesterday)
    df_merged["Rank_Change"] = df_merged["Yesterday_Rank"] - df_merged["Rank"]

    # Display the complete leaderboard
    st.table(df_merged[["Rank", "username", "cumulative_points", "Yesterday_Rank", "Rank_Change"]].rename(
        columns={
            "username": "User",
            "cumulative_points": "Today's Points",
            "Yesterday_Rank": "Yesterday's Rank",
            "Rank_Change": "Rank Change"
        }
    ))

    # Search functionality: allow user to input a username
    st.subheader("Search Your Ranking")
    search_username = st.text_input("Enter your username to search:")
    if search_username:
        user_data = df_merged[df_merged["username"].str.lower() == search_username.lower()]
        if not user_data.empty:
            st.write(user_data[["Rank", "username", "cumulative_points", "Yesterday_Rank", "Rank_Change"]].rename(
                columns={
                    "username": "User",
                    "cumulative_points": "Today's Points",
                    "Yesterday_Rank": "Yesterday's Rank",
                    "Rank_Change": "Rank Change"
                }
            ))
        else:
            st.info("Username not found in the leaderboard.")

if __name__ == "__main__":
    main()
