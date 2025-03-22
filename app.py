import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------
# Emission Factors (kg CO2)
# ------------------------------
CAR_CO2_PER_KM = 0.25          # Car emissions per km
BUS_CO2_PER_KM = 0.10          # Bus emissions per km per person
ELECTRICITY_CO2_PER_KWH = 0.42 # Electricity emissions per kWh (NJ grid)

# ------------------------------
# Total Emissions for New Jersey (simulated data)
# ------------------------------
NJ_TOTAL_EMISSIONS_MT = 80e6   # 80 million metric tons CO2

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
    """Interactive calculator for individual carbon emissions."""
    st.header("Personal Carbon Footprint Calculator")
    st.write("Enter your daily commute and electricity usage. Earn reward points for low-carbon habits.")

    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox("Transportation Mode", ["Car", "Bus"])
        distance = st.number_input("Travel Distance (km)", min_value=0.0, value=0.0, step=0.1)
    with col2:
        electricity_usage = st.number_input("Daily Electricity Usage (kWh)", min_value=0.0, value=0.0, step=0.1)

    # Emissions calculations
    transport_emission = distance * (CAR_CO2_PER_KM if mode == "Car" else BUS_CO2_PER_KM)
    electricity_emission = electricity_usage * ELECTRICITY_CO2_PER_KWH
    total_emission = transport_emission + electricity_emission

    # Display results
    st.subheader("Your Daily Carbon Emissions")
    st.write(f"**Transport Emissions**: {transport_emission:.2f} kg CO₂")
    st.write(f"**Electricity Emissions**: {electricity_emission:.2f} kg CO₂")
    st.write(f"**Total Emissions**: {total_emission:.2f} kg CO₂")

    # Reward points logic
    baseline = 10  # kg CO₂ per day
    points = calculate_reward_points(total_emission, baseline)

    st.subheader("Reward Points")
    st.write(f"Points earned today: **{points:.0f} points**")
    st.info("Tip: Choose low-carbon transport and conserve electricity to earn more points!")

    # Trend visualization (mockup)
    st.subheader("Example Emission Trend")
    df_trend = pd.DataFrame({"Time": ["Today"], "Emissions (kg CO₂)": [total_emission]})
    fig_trend = px.bar(df_trend, x="Time", y="Emissions (kg CO₂)", color="Emissions (kg CO₂)",
                       title="Today's Emission Trend")
    st.plotly_chart(fig_trend)

def calculate_reward_points(emission: float, baseline: float = 10.0) -> float:
    """Calculate reward or penalty points based on carbon emissions."""
    if emission <= baseline:
        return (baseline - emission) * 10
    return - (emission - baseline) * 5

def nj_overview():
    """Overview of state-level carbon emissions."""
    st.header("New Jersey State Overview")
    st.write("Simulated heatmap of county-level carbon emissions across NJ.")
    st.write(f"**Total CO₂ Emissions for New Jersey**: {NJ_TOTAL_EMISSIONS_MT / 1e6:.1f} million metric tons")

    county_data = pd.DataFrame({
        "County": ["Bergen", "Essex", "Hudson", "Middlesex", "Monmouth", "Ocean", "Union", "Camden"],
        "lat": [40.926, 40.735, 40.728, 40.560, 40.300, 39.900, 40.652, 39.950],
        "lon": [-74.077, -74.264, -74.032, -74.350, -74.010, -74.260, -74.270, -75.100],
        "Emissions": [12, 15, 18, 10, 8, 7, 9, 11]  # in million tons
    })

    st.subheader("County-Level Emissions Heatmap")
    fig = px.scatter_mapbox(
        county_data,
        lat="lat",
        lon="lon",
        size="Emissions",
        color="Emissions",
        hover_name="County",
        hover_data={"Emissions": True, "lat": False, "lon": False},
        zoom=7,
        height=500,
        title="Heatmap of County Emission Indicators"
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig)

def leaderboard():
    """Leaderboard view of users with most eco points."""
    st.header("Points Leaderboard")
    st.write("Simulated leaderboard based on eco-points earned by users:")

    leaderboard_data = pd.DataFrame({
        "User": ["Alice", "Bob", "Charlie", "David", "Eva"],
        "Points": [150, 120, 95, 80, 70]
    })
    st.table(leaderboard_data)

if __name__ == "__main__":
    main()