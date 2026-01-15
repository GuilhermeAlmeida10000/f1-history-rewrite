import streamlit as st
import pandas as pd
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="F1 History Explorer",
    page_icon="🏎️",
    layout="wide"
)

# --- 2. CONSTANTS & UTILS ---
CURRENT_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

NAT_TO_FLAG = {
    'British': '🇬🇧', 'German': '🇩🇪', 'Brazilian': '🇧🇷', 'French': '🇫🇷', 
    'Finnish': '🇫🇮', 'Italian': '🇮🇹', 'Spanish': '🇪🇸', 'Austrian': '🇦🇹', 
    'American': '🇺🇸', 'Japanese': '🇯🇵', 'Australian': '🇦🇺', 'Canadian': '🇨🇦', 
    'Dutch': '🇳🇱', 'Belgian': '🇧🇪', 'Monegasque': '🇲🇨', 'Swiss': '🇨🇭', 
    'Swedish': '🇸🇪', 'New Zealander': '🇳🇿', 'Mexican': '🇲🇽', 'Argentine': '🇦🇷', 
    'South African': '🇿🇦', 'Colombian': '🇨🇴', 'Venezuelan': '🇻🇪', 'Danish': '🇩🇰', 
    'Russian': '🇷🇺', 'Polish': '🇵🇱', 'Portuguese': '🇵🇹', 'Irish': '🇮🇪',
    'Chinese': '🇨🇳', 'Thai': '🇹🇭', 'Indonesian': '🇮🇩'
}

def get_flag(nationality):
    return NAT_TO_FLAG.get(nationality, "🌍")

def calculate_modern_points(position):
    try:
        return CURRENT_POINTS.get(int(position), 0)
    except:
        return 0

# --- 3. DATA LOADING (CACHED & RENAMED) ---
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "data")
    
    try:
        # Load Races
        races = pd.read_csv(os.path.join(data_path, "races.csv"), encoding='utf-8-sig', 
                           header=0, names=['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url'], 
                           usecols=[0,1,2,3,4,5,6,7])
        
        # FIX: Rename 'name' to 'race_name' to avoid conflict
        races.rename(columns={'name': 'race_name'}, inplace=True)

        results = pd.read_csv(os.path.join(data_path, "results.csv"), encoding='utf-8-sig')
        drivers = pd.read_csv(os.path.join(data_path, "drivers.csv"), encoding='utf-8-sig')
        constructors = pd.read_csv(os.path.join(data_path, "constructors.csv"), encoding='utf-8-sig')
        
        # FIX: Rename 'name' to 'team_name' and 'nationality' to 'team_nat'
        constructors.rename(columns={'name': 'team_name', 'nationality': 'team_nat'}, inplace=True)
        
        # Clean whitespaces
        for df in [races, results, drivers, constructors]:
            df.columns = df.columns.str.strip()
            
        races['year'] = pd.to_numeric(races['year'], errors='coerce')
        return races, results, drivers, constructors
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None, None, None, None

races, results, drivers, constructors = load_data()

# --- 4. SIDEBAR CONFIG ---
st.sidebar.header("🏁 Configuration")
st.sidebar.markdown("Recalculate F1 championships using the **2024 Scoring System**.")

if races is not None:
    available_years = sorted(races[races['year'] < 2010]['year'].unique().astype(int), reverse=True)
    default_index = available_years.index(2008) if 2008 in available_years else 0
    selected_year = st.sidebar.selectbox("Select Season", available_years, index=default_index)
else:
    selected_year = 2008

st.sidebar.markdown("---")
st.sidebar.markdown("Developed by **Guilherme Almeida**")

# --- 5. MAIN LOGIC ---
if races is not None:
    # Filter Data
    races_year = races[races['year'] == selected_year].sort_values('round')
    race_ids = races_year['raceId'].tolist()
    
    results_year = results[results['raceId'].isin(race_ids)].copy()
    
    # Calculate Points
    results_year['positionOrder'] = pd.to_numeric(results_year['positionOrder'], errors='coerce')
    results_year['modern_points'] = results_year['positionOrder'].apply(calculate_modern_points)
    
    # Merge Data (Now using the new column names)
    full_data = results_year.merge(drivers, on='driverId')
    full_data = full_data.merge(constructors, on='constructorId') # No suffixes needed for name now
    full_data = full_data.merge(races_year[['raceId', 'race_name', 'round']], on='raceId')
    
    # --- 6. CHART DATA PREP ---
    # Pivot for chart
    pivot_points = full_data.pivot_table(index='round', columns='surname', values='modern_points', aggfunc='sum').fillna(0)
    cumulative_points = pivot_points.cumsum()
    
    # Top 10 for Chart
    top_10_drivers = cumulative_points.iloc[-1].sort_values(ascending=False).head(10).index
    chart_data = cumulative_points[top_10_drivers]
    
    # --- 7. UI: HEADER ---
    st.title(f"🏎️ F1 Season {selected_year}: The Modern Rewrite")
    
    final_scores = cumulative_points.iloc[-1].sort_values(ascending=False)
    champion_surname = final_scores.index[0]
    runner_up_surname = final_scores.index[1]
    
    # Get Champion Full Info
    champ_row = full_data[full_data['surname'] == champion_surname].iloc[0]
    champ_flag = get_flag(champ_row['nationality']) # Driver nationality
    champ_full_name = f"{champ_row['forename']} {champ_row['surname']}"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Rewritten Champion", f"{champ_flag} {champ_full_name}")
    col2.metric("🥈 Runner-up", runner_up_surname)
    col3.metric("🔥 Gap", f"{int(final_scores[champion_surname] - final_scores[runner_up_surname])} pts")
    
    st.divider()
    
    # --- 8. UI: CHART ---
    st.subheader("📈 Season Evolution (Top 10)")
    st.markdown("Cumulative points race by race.")
    st.line_chart(chart_data)
    
    st.divider()
    
    # --- 9. UI: TABLE ---
    st.subheader("📊 Final Standings")

    # Group by Driver Info
    standings = full_data.groupby(['driverId', 'forename', 'surname', 'nationality'])['modern_points'].sum().reset_index()
    
    # Function to build Team String
    def get_driver_team_str(d_id):
        # Now looking for 'team_name' and 'team_nat' (Renamed in load_data)
        teams = full_data[full_data['driverId'] == d_id][['team_name', 'team_nat']].drop_duplicates()
        if teams.empty: return "Unknown"
        
        formatted_teams = []
        for _, row in teams.iterrows():
            # Flag + Team Name
            t_flag = get_flag(row['team_nat'])
            formatted_teams.append(f"{t_flag} {row['team_name']}")
            
        return ", ".join(formatted_teams)

    # Apply formatting
    # Driver: Flag + Forename + Surname
    standings['Driver'] = standings.apply(lambda x: f"{get_flag(x['nationality'])} {x['forename']} {x['surname']}", axis=1)
    
    # Team: Flag + Team Name
    standings['Team'] = standings['driverId'].apply(get_driver_team_str)
    
    # Sort and Index
    standings = standings.sort_values('modern_points', ascending=False).reset_index(drop=True)
    standings.index += 1
    
    # Select columns
    final_display = standings[['Driver', 'Team', 'modern_points']]
    final_display.columns = ['Driver', 'Team', 'Points']

    st.dataframe(final_display, use_container_width=True)

else:
    st.warning("Data not loaded. Check your 'data' folder.")