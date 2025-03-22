# Carbon_tracker
An Web tool for tracking the Carbon in the NJ, and contributing to cu down the Carbon-dioxide
An Web tool for tracking the Carbon in the NJ, and contributing to cu down the Carbon-dioxide

Below is a complete README in Markdown format for the project:

⸻

City Carbon Footprint Tracker + Citizen Rewards System

Overview

This project is an interactive web application built using Streamlit. It tracks the daily carbon footprint of users in New Jersey by calculating emissions from transportation and electricity usage. Users can view simulated emission trends, earn reward points by reducing their emissions below the NJ per capita average, and compare their performance on a dynamic leaderboard.

Features
	•	Personal Carbon Calculator:
	•	Users input daily commute details (transportation mode and travel distance) and electricity usage.
	•	The app calculates carbon emissions using preset emission factors.
	•	Reward points are assigned based on how the user’s emissions compare with the NJ per capita daily average (25 kg CO₂).
	•	A simulated 7-day emission trend chart helps users visualize their progress.
	•	NJ Overview:
	•	Displays a detailed, NJ-only map with simulated county-level carbon emissions for all 21 NJ counties.
	•	An interactive slider lets users filter counties based on a minimum emission threshold.
	•	Leaderboard:
	•	Users’ cumulative eco-points are tracked and ranked.
	•	The leaderboard shows each user’s current ranking, ranking change compared to yesterday, and allows for quick username searches.

Data and Assumptions
	•	Emission Factors (kg CO₂/km):
	•	Car: 0.25
	•	Bus: 0.10
	•	Train: 0.06 (typical value for intercity trains)
	•	Subway: 0.05 (urban rail systems are very energy efficient)
	•	Bicycle: 0.0
	•	Walking: 0.0
	•	Electricity Emission Factor: 0.42 kg CO₂ per kWh (NJ grid estimate)
	•	NJ Per Capita Daily Emission: Approximately 25 kg CO₂ per day
	•	Total NJ Emissions (simulated): 80 million metric tons CO₂
	•	County Data:
Simulated data for 21 NJ counties (including approximate latitude and longitude values) is used for the detailed NJ map.

Requirements
	•	Python 3.7 or higher
	•	Streamlit
	•	Pandas
	•	NumPy
	•	Plotly Express

Install the required packages via pip:

pip install streamlit pandas numpy plotly

Installation and Running
	1.	Clone the Repository:

git clone <repository_url>
cd <repository_folder>


	2.	Run the Application: Streamlit run app.py



The application will launch in your default web browser.

Project Structure
	•	app.py:
Main application file containing the complete code for the interactive Streamlit app.
	•	user_points.txt:
A CSV file (automatically created and updated) used to store users’ cumulative reward points and track ranking changes.

Usage
	•	Personal Carbon Calculator:
	•	Enter your username, select a transportation mode, input travel distance and daily electricity usage.
	•	View your daily carbon emissions and reward points.
	•	Check the 7-day emission trend chart to visualize your performance over time.
	•	Optionally view emission reduction tips and a progress gauge indicating your performance relative to a target.
	•	NJ Overview:
	•	Explore a detailed map of New Jersey with markers for all 21 counties.
	•	Use the interactive slider to filter counties by their emission levels.
	•	Leaderboard:
	•	View the ranking of all users based on cumulative eco-points.
	•	See how your ranking has changed compared to yesterday.
	•	Use the search functionality to quickly locate your ranking.

Future Improvements
	•	Data Integration:
Incorporate real-world emission data for increased accuracy.
	•	User Authentication:
Implement secure user accounts for personalized tracking.
	•	Enhanced Visualization:
Improve data visualizations and mobile responsiveness.
	•	Feature Expansion:
Add additional interactive features, such as detailed tips and comparison tools.

License

This project is licensed under the MIT License.

Credits

Developed by [Your Name] as part of a hackathon project. Special thanks to contributors and data sources that provided emission factor estimates and NJ environmental data.

⸻

Feel free to contribute, open issues, or provide feedback!
