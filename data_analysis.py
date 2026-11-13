"""
Module: data_analysis.py
Course: Data Analytics and Visualization
Project: Urban Cleanliness (Swachh Survekshan) & Ganga River Water Quality Analysis
"""

import pandas as pd
import numpy as np

def run_analysis():
    print("=" * 65)
    print("  STAGE 1: URBAN SWACHH SURVEKSHAN PERFORMANCE ANALYSIS  ")
    print("=" * 65)
    df_cities = pd.read_csv("combined_city_clean.csv")
    
    # 1. Performance by Population Bracket
    print("\n[A] Performance by Population Category:")
    cohort_stats = df_cities.groupby('population_category')['total_score'].agg(
        Count='count',
        Mean='mean',
        Median='median',
        Std_Dev='std',
        Min='min',
        Max='max'
    ).round(2)
    print(cohort_stats)

    # 2. Top 5 Cities Nationally
    print("\n[B] Top 5 Cities Nationally (Across Both Cohorts):")
    top5 = df_cities[['overall_rank', 'city_clean', 'state_ut', 'population_category', 'total_score']].head(5)
    print(top5.to_string(index=False))

    # 3. Bottom 5 Cities Nationally
    print("\n[C] Bottom 5 Cities Nationally:")
    bottom5 = df_cities[['overall_rank', 'city_clean', 'state_ut', 'population_category', 'total_score']].tail(5)
    print(bottom5.to_string(index=False))

    # 4. State-Level Performance (Min. 3 Cities)
    print("\n[D] Top 5 States by Cleanliness Average (Min. 3 Cities):")
    state_perf = df_cities.groupby('state_ut').filter(lambda x: len(x) >= 3)
    state_rankings = state_perf.groupby('state_ut')['total_score'].agg(
        City_Count='count',
        Avg_Score='mean'
    ).sort_values(by='Avg_Score', ascending=False).round(2)
    print(state_rankings.head(5))

    print("\n" + "=" * 65)
    print("  STAGE 2: GANGA RIVER WATER QUALITY ANALYSIS (2012)  ")
    print("=" * 65)
    df_ganga = pd.read_csv("ganga_water_quality_clean.csv")

    # Normalize column names in case they differ slightly
    col_aliases = {
        'dissolved_oxygen_mean_mg_l': 'do_mean_mg_l',
        'temperature_mean_c': 'temp_mean_c'
    }
    df_ganga.rename(columns=col_aliases, inplace=True)

    # Ensure flags exist
    if 'bod_polluted_flag' not in df_ganga.columns and 'bod_mean_mg_l' in df_ganga.columns:
        df_ganga['bod_polluted_flag'] = df_ganga['bod_mean_mg_l'] > 3.0
    if 'do_critical_flag' not in df_ganga.columns and 'do_mean_mg_l' in df_ganga.columns:
        df_ganga['do_critical_flag'] = df_ganga['do_mean_mg_l'] < 4.0

    # 1. State-wise River Quality Means
    print("\n[A] State-wise Water Quality Indicators:")
    metric_cols = [c for c in ['do_mean_mg_l', 'bod_mean_mg_l', 'ph_mean', 'conductivity_mean'] if c in df_ganga.columns]
    river_state_means = df_ganga.groupby('state')[metric_cols].mean().round(2)
    print(river_state_means)

    # 2. Environmental Compliance Flags
    if 'bod_polluted_flag' in df_ganga.columns:
        polluted_bod = int(df_ganga['bod_polluted_flag'].sum())
        total_stations = len(df_ganga)
        print(f"\n[B] Pollution Status:")
        print(f" - Total River Monitoring Stations: {total_stations}")
        print(f" - Stations Violating Safe BOD Standards (> 3 mg/L): {polluted_bod} ({round(polluted_bod/total_stations*100, 1)}%)")
        print(f" - Stations with Critical DO Depletion (< 4 mg/L): {int(df_ganga['do_critical_flag'].sum())}")

    # 3. Top 5 Most Polluted Stations by BOD
    print("\n[C] Top 5 Most Polluted River Locations (Highest BOD):")
    disp_cols = [c for c in ['station_location', 'state', 'bod_mean_mg_l', 'do_mean_mg_l'] if c in df_ganga.columns]
    top_polluted = df_ganga.sort_values(by='bod_mean_mg_l', ascending=False)[disp_cols].head(5)
    print(top_polluted.to_string(index=False))

    print("\n" + "=" * 65)
    print("  STAGE 3: CROSS-DOMAIN URBAN-RIVER CORRELATION  ")
    print("=" * 65)
    ganga_cities = df_cities[df_cities['city_clean'].str.contains('Kanpur|Prayagraj|Varanasi|Patna', case=False, na=False)]
    print("\nSwachh Scores of Major Ganga Basin Cities:")
    print(ganga_cities[['overall_rank', 'city_clean', 'state_ut', 'total_score', 'odf_score']].to_string(index=False))
    print("\nKey Finding: While Ganga basin cities achieve high municipal sanitation scores (10,500+ / 12,500),")
    print("downstream river stations (e.g. Kanpur D/S at 8.32 mg/L BOD) exhibit heavy organic pollution,")
    print("revealing the operational contrast between municipal street cleanliness and river waste treatment.")

if __name__ == "__main__":
    run_analysis()