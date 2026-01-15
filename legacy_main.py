import pandas as pd
import os
import sys

# --- 1. SETTINGS & FLAGS ---
CURRENT_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

# Flags Mapping
NAT_TO_FLAG = {
    'British': '🇬🇧', 'German': '🇩🇪', 'Brazilian': '🇧🇷', 'French': '🇫🇷', 
    'Finnish': '🇫🇮', 'Italian': '🇮🇹', 'Spanish': '🇪🇸', 'Austrian': '🇦🇹', 
    'American': '🇺🇸', 'Japanese': '🇯🇵', 'Australian': '🇦🇺', 'Canadian': '🇨🇦', 
    'Dutch': '🇳🇱', 'Belgian': '🇧🇪', 'Monegasque': '🇲🇨', 'Swiss': '🇨🇭', 
    'Swedish': '🇸🇪', 'New Zealander': '🇳🇿', 'Mexican': '🇲🇽', 'Argentine': '🇦🇷', 
    'South African': '🇿🇦', 'Colombian': '🇨🇴', 'Venezuelan': '🇻🇪', 'Danish': '🇩🇰', 
    'Russian': '🇷🇺', 'Polish': '🇵🇱', 'Portuguese': '🇵🇹', 'Irish': '🇮🇪',
    'Indian': '🇮🇳', 'Thai': '🇹🇭', 'Indonesian': '🇮🇩', 'Hungarian': '🇭🇺',
    'Malaysian': '🇲🇾', 'Chilean': '🇨🇱', 'Uruguayan': '🇺🇾', 'Rhodesian': '🇿🇼',
    'Chinese': '🇨🇳'
}

COUNTRY_TO_FLAG = {
    'UK': '🇬🇧', 'Germany': '🇩🇪', 'Brazil': '🇧🇷', 'France': '🇫🇷', 
    'Italy': '🇮🇹', 'Spain': '🇪🇸', 'Austria': '🇦🇹', 'USA': '🇺🇸', 'United States': '🇺🇸',
    'Japan': '🇯🇵', 'Australia': '🇦🇺', 'Canada': '🇨🇦', 'Netherlands': '🇳🇱', 
    'Belgium': '🇧🇪', 'Monaco': '🇲🇨', 'Switzerland': '🇨🇭', 'Sweden': '🇸🇪', 
    'Mexico': '🇲🇽', 'Argentina': '🇦🇷', 'South Africa': '🇿🇦', 'Russia': '🇷🇺',
    'Portugal': '🇵🇹', 'India': '🇮🇳', 'Turkey': '🇹🇷', 'Malaysia': '🇲🇾',
    'China': '🇨🇳', 'Bahrain': '🇧🇭', 'Singapore': '🇸🇬', 'UAE': '🇦🇪', 
    'Korea': '🇰🇷', 'Azerbaijan': '🇦🇿', 'Hungary': '🇭🇺', 'Saudi Arabia': '🇸🇦',
    'Qatar': '🇶🇦', 'Morocco': '🇲🇦', 'Vietnam': '🇻🇳'
}

def get_flag(nationality, is_country=False):
    repo = COUNTRY_TO_FLAG if is_country else NAT_TO_FLAG
    return repo.get(nationality, "🌍")

def calculate_modern_points(position):
    try:
        return CURRENT_POINTS.get(int(position), 0)
    except:
        return 0
    

# Smart Padding Function
def smart_pad(text, width, align='left'):
    text = str(text)
    # Emojis count as 1 or 2 characters depending on the system,
    # but visually occupy 2. This attempts to compensate.
    visible_len = len(text) 
    spaces = max(0, width - visible_len)
    
    if align == 'left':
        return text + (" " * spaces)
    else:
        return (" " * spaces) + text

# --- 2. LOADING DATA ---
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data")
output_dir = os.path.join(script_dir, "seasons_data")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"📂 Loading data from: {data_path}")

try:
    # Careful reading with proper encoding and column names
    races = pd.read_csv(os.path.join(data_path, "races.csv"), encoding='utf-8-sig', 
                       header=0, names=['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url'], 
                       usecols=[0,1,2,3,4,5,6,7])
    races['year'] = pd.to_numeric(races['year'], errors='coerce')
    
    results = pd.read_csv(os.path.join(data_path, "results.csv"), encoding='utf-8-sig')
    drivers = pd.read_csv(os.path.join(data_path, "drivers.csv"), encoding='utf-8-sig')
    constructors = pd.read_csv(os.path.join(data_path, "constructors.csv"), encoding='utf-8-sig')
    circuits = pd.read_csv(os.path.join(data_path, "circuits.csv"), encoding='utf-8-sig')

    for df in [results, drivers, constructors, circuits]:
        df.columns = df.columns.str.strip()

    print("✅ Data loaded successfully.")

except Exception as e:
    print(f"❌ Fatal Error: {e}")
    sys.exit()

# --- 3. PROCESSING ---
years = sorted(races['year'].dropna().unique().astype(int))
years_to_process = [y for y in years if y < 2010]

print(f"🚀 Processing {len(years_to_process)} seasons...")

for year in years_to_process:
    races_year = races[races['year'] == year]
    race_ids = races_year['raceId'].tolist()
    
    if not race_ids:
        continue

    results_year = results[results['raceId'].isin(race_ids)].copy()

    # Preparing Auxiliary Data
    circuit_ids = races_year['circuitId'].unique()
    circuits_year = circuits[circuits['circuitId'].isin(circuit_ids)].copy()
    circuits_year['display'] = circuits_year.apply(lambda x: f"{get_flag(x['country'], True)} {x['name']} ({x['country']})", axis=1)
    
    constructor_ids = results_year['constructorId'].unique()
    constructors_year = constructors[constructors['constructorId'].isin(constructor_ids)].copy()
    constructors_year['display'] = constructors_year.apply(lambda x: f"{get_flag(x['nationality'])} {x['name']}", axis=1)

    # Preparing Main Table
    results_year['positionOrder'] = pd.to_numeric(results_year['positionOrder'], errors='coerce')
    results_year['modern_points'] = results_year['positionOrder'].apply(calculate_modern_points)
    
    full_data = results_year.merge(drivers, on='driverId')
    full_data = full_data.merge(constructors, on='constructorId', suffixes=('_dr', '_co'))
    
    standings = full_data.groupby(['driverId', 'forename', 'surname', 'nationality_dr'])['modern_points'].sum().reset_index()
    
    def get_driver_team(d_id):
        teams = full_data[full_data['driverId'] == d_id][['name', 'nationality_co']].drop_duplicates()
        if teams.empty: return "Unknown"
        formatted_teams = []
        for _, row in teams.iterrows():
            formatted_teams.append(f"{get_flag(row['nationality_co'])} {row['name']}")
        return ", ".join(formatted_teams)

    # Creating final display columns
    standings['pos_display'] = "" # Will be filled after sorting
    standings['driver_display'] = standings.apply(lambda x: f"{get_flag(x['nationality_dr'])} {x['forename']} {x['surname']}", axis=1)
    standings['team_display'] = standings['driverId'].apply(get_driver_team)
    standings = standings.sort_values('modern_points', ascending=False).reset_index(drop=True)
    standings.index += 1

    # Filling positions (1st, 2nd...)
    standings['pos_display'] = standings.index.astype(str) + "º"
    standings['pts_display'] = standings['modern_points'].astype(str)

    # --- DYNAMIC WIDTH CALCULATION ---
    w_pos = max(standings['pos_display'].apply(len).max(), 3) + 2
    w_driver = max(standings['driver_display'].apply(len).max(), 6) + 3
    w_team = max(standings['team_display'].apply(len).max(), 4) + 3
    w_pts = max(standings['pts_display'].apply(len).max(), 3) + 2

    # --- WRITING MD FILE ---
    filename = os.path.join(output_dir, f"S{year}.md")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🏎️ F1 SEASON {year} - REWRITE\n\n")
        f.write(f"> 2024 Scoring System Applied.\n\n")
        
        # Circuits List (Bullet points don't need padding logic)
        f.write("## 🌍 Circuits\n")
        for item in circuits_year['display']:
            f.write(f"- {item}\n")
        f.write("\n")
        
        # Teams List
        f.write("## 🛠️ Teams\n")
        for item in constructors_year['display']:
            f.write(f"- {item}\n")
        f.write("\n")
        
        # TABLE GENERATION
        f.write("## 🏆 Final Standings\n\n")
        
        # Header
        header = f"| {smart_pad('Pos', w_pos)} | {smart_pad('Driver', w_driver)} | {smart_pad('Team', w_team)} | {smart_pad('Pts', w_pts, 'right')} |"
        f.write(header + "\n")
        
        # Separator (Dynamic length)
        separator = f"| {smart_pad(':-:', w_pos)} | {smart_pad(':-', w_driver)} | {smart_pad(':-', w_team)} | {smart_pad('-:', w_pts, 'right')} |"
        f.write(separator + "\n")
        
        # Rows
        for _, row in standings.iterrows():
            line = f"| {smart_pad(row['pos_display'], w_pos)} | {smart_pad(row['driver_display'], w_driver)} | {smart_pad(row['team_display'], w_team)} | {smart_pad(row['pts_display'], w_pts, 'right')} |"
            f.write(line + "\n")
            
        # Champion Info
        champ = standings.iloc[0]
        f.write(f"\n**👑 CHAMPION:** {champ['driver_display']} ({champ['pts_display']} pts)\n")
        
print(f"\n✨ DONE! Check the 'seasons_data' folder.")