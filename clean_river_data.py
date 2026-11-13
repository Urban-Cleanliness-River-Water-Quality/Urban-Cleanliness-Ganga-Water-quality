import pandas as pd

def clean_ganga_data():
    print("[2/3] Loading and cleaning Ganga river dataset...")
    # Encoding latin1 is required for micro-siemens symbol (µmhos/cm)
    df_ganga = pd.read_csv("water_quality_2012_river_ganga uncleaned.csv", encoding="latin1")

    # Clean and simplify column names
    df_ganga.columns = [c.strip() for c in df_ganga.columns]

    # Select the mean/core columns for streamlined analysis
    selected_cols = {
        'STATION CODE': 'station_code',
        'LOCATIONS': 'station_location',
        'STATE': 'state',
        'TEMPERATURE in degree Centigrade] - Mean': 'temperature_mean_c',
        'D.O. (mg/l) [> 4 mg/l] - Mean': 'dissolved_oxygen_mean_mg_l',
        'pH [6.5-8.5] - Mean': 'ph_mean',
        'CONDUCTIVITY (µmhos/cm)] - Mean': 'conductivity_mean',
        'B.O.D. (mg/l) [< 3 mg/l] - Mean': 'bod_mean_mg_l',
        'NITRATE- N+ NITRITE-N (mg/l)] - Mean': 'nitrate_nitrite_mean_mg_l',
        'FECAL COLIFORM (MPN/100ml) [< 2500 MPN/100ml] - Mean': 'fecal_coliform_mean_mpn_100ml',
        'TOTAL COLIFORM (MPN/100ml) [< 5000 MPN/100ml] - Mean': 'total_coliform_mean_mpn_100ml'
    }

    df_ganga_clean = df_ganga[list(selected_cols.keys())].rename(columns=selected_cols)
    df_ganga_clean['state'] = df_ganga_clean['state'].astype(str).str.title().str.strip()
    df_ganga_clean['station_location'] = df_ganga_clean['station_location'].astype(str).str.title().str.strip()

    output_file = "ganga_water_quality_clean.csv"
    df_ganga_clean.to_csv(output_file, index=False)
    print(f"[Done] Cleaned river dataset saved to '{output_file}' with {len(df_ganga_clean)} monitoring stations!")

if __name__ == "__main__":
    clean_ganga_data()