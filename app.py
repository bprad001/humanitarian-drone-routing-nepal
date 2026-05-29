import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Sindhupalchok Drone Network")

st.title(" Sindhupalchok Drone Optimization Dashboard")

# 1. Load the finalized analytics data
@st.cache_data
def load_data():
    return pd.read_csv("data/sindhupalchok_final_analytics.csv")

df = load_data()

# Find coordinate columns safely
lat_col = [c for c in df.columns if c.lower() in ['latitude', 'lat', 'y']][0]
lon_col = [c for c in df.columns if c.lower() in ['longitude', 'lon', 'x']][0]

# 2. Sidebar Inputs
st.sidebar.header(" Operational Parameters")
base_range = st.sidebar.slider("Base Flight Range (km)", 40, 150, 80)
base_speed = st.sidebar.slider("Base Cruise Speed (km/h)", 50, 150, 100)

st.sidebar.header(" Environmental Factors")
monsoon_penalty = st.sidebar.slider(
    "Monsoon Weather Penalty (%)", 0, 50, 0, 
    help="High winds and heavy rain reduce battery efficiency and speed."
)

# Apply Weather Penalties
effective_range = base_range * (1 - (monsoon_penalty / 100.0))
effective_speed = base_speed * (1 - (monsoon_penalty / 100.0))

st.sidebar.markdown(f"**Effective Range:** {effective_range:.1f} km")
st.sidebar.markdown(f"**Effective Speed:** {effective_speed:.1f} km/h")

# 3. Dynamic Calculations based on sliders
df['is_covered'] = df['Drone_Distance_km'] <= effective_range
df['Dynamic_Drone_Time_hrs'] = df['Drone_Distance_km'] / effective_speed

# Only calculate savings for clinics the drone can actually reach!
covered_clinics = df[df['is_covered']]
coverage_pct = (len(covered_clinics) / len(df)) * 100

total_time_saved = covered_clinics['Truck_Time_hrs'].sum() - covered_clinics['Dynamic_Drone_Time_hrs'].sum()
total_money_saved = covered_clinics['Money_Saved_USD'].sum()

# 4. Top Metrics Display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Coverage Score", f"{coverage_pct:.1f}%")
col2.metric("Clinics Reached", f"{len(covered_clinics)} / {len(df)}")
col3.metric("Total Time Saved", f"{total_time_saved:.1f} Hours")
col4.metric("Total Money Saved", f"${total_money_saved:.2f}")

# 5. Build Map
m = folium.Map(location=[df[lat_col].mean(), df[lon_col].mean()], zoom_start=11, tiles="CartoDB positron")

# Plot the Optimized Hub (Blue Star)
hub_id = int(df.iloc[0]['Optimized_Hub_ID'])
hub_lat = df.iloc[hub_id][lat_col]
hub_lon = df.iloc[hub_id][lon_col]

folium.Marker(
    location=[hub_lat, hub_lon],
    icon=folium.Icon(color="blue", icon="star"),
    popup="<b> OPTIMIZED DRONE HUB</b>"
).add_to(m)

# Plot Clinics
for idx, row in df.iterrows():
    if idx == hub_id: continue # Don't plot over the hub
    color = "green" if row['is_covered'] else "red"
    
    # Popup text comparing Truck vs Drone
    popup_text = f"""
    <b>{row.get('name', 'Clinic')}</b><br>
    Truck Drive: {row['Truck_Time_hrs']:.1f} hrs<br>
    Drone Flight: {row['Dynamic_Drone_Time_hrs']:.1f} hrs
    """
    
    folium.CircleMarker(
        location=[row[lat_col], row[lon_col]],
        radius=6, color=color, fill=True, fill_opacity=0.7,
        popup=popup_text
    ).add_to(m)

st_folium(m, width=1400, height=500)

# 6. Download Data Button
st.write("### Export Active Analytics Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=" Download Results as CSV",
    data=csv,
    file_name='sindhupalchok_dashboard_results.csv',
    mime='text/csv',
)


