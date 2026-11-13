"""
Module: data_visualisation.py
Course: Data Analytics and Visualization
Description: Generates multi-panel comparative analytical charts for presentation and report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations():
    print("[1/2] Loading datasets for plotting...")
    df_cities = pd.read_csv("combined_city_clean.csv")
    df_ganga = pd.read_csv("ganga_water_quality_clean.csv")

    # Safeguard column aliases
    col_aliases = {
        'dissolved_oxygen_mean_mg_l': 'do_mean_mg_l',
        'temperature_mean_c': 'temp_mean_c'
    }
    df_ganga.rename(columns=col_aliases, inplace=True)

    if 'bod_polluted_flag' not in df_ganga.columns and 'bod_mean_mg_l' in df_ganga.columns:
        df_ganga['bod_polluted_flag'] = df_ganga['bod_mean_mg_l'] > 3.0
    if 'do_critical_flag' not in df_ganga.columns and 'do_mean_mg_l' in df_ganga.columns:
        df_ganga['do_critical_flag'] = df_ganga['do_mean_mg_l'] < 4.0

    sns.set_theme(style="whitegrid", palette="muted")
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))

    # --- Chart 1: Population Category vs Total Score (Boxplot) ---
    sns.boxplot(
        data=df_cities,
        x='population_category',
        y='total_score',
        palette=['#3498db', '#2ecc71'],
        ax=axes[0, 0]
    )
    axes[0, 0].set_title("1. Urban Cleanliness Distribution by Population Tier", fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel("Population Cohort")
    axes[0, 0].set_ylabel("Total Score (Max 12,500)")

    # --- Chart 2: Top 10 Ranked Cities Overall (Horizontal Bar) ---
    top10_cities = df_cities.sort_values(by='overall_rank').head(10)
    sns.barplot(
        data=top10_cities,
        x='total_score',
        y='city_clean',
        palette='Blues_r',
        ax=axes[0, 1]
    )
    axes[0, 1].set_title("2. Top 10 Cleanest Cities Nationally", fontsize=13, fontweight='bold')
    axes[0, 1].set_xlabel("Total Score")
    axes[0, 1].set_ylabel("City")

    # --- Chart 3: Ganga River B.O.D. Pollution by State (Barplot) ---
    state_bod = df_ganga.groupby('state')['bod_mean_mg_l'].mean().reset_index()
    sns.barplot(
        data=state_bod,
        x='state',
        y='bod_mean_mg_l',
        palette='Reds_r',
        ax=axes[1, 0]
    )
    axes[1, 0].axhline(3.0, color='red', linestyle='--', linewidth=1.5, label='Safe BOD Limit (< 3 mg/L)')
    axes[1, 0].set_title("3. Average Biochemical Oxygen Demand (B.O.D.) by River State", fontsize=13, fontweight='bold')
    axes[1, 0].set_xlabel("River Stretch State")
    axes[1, 0].set_ylabel("B.O.D. (mg/L)")
    axes[1, 0].legend()

    # --- Chart 4: Dissolved Oxygen (D.O.) vs B.O.D. Scatter Plot ---
    sns.scatterplot(
        data=df_ganga,
        x='bod_mean_mg_l',
        y='do_mean_mg_l',
        hue='state',
        style='bod_polluted_flag',
        s=90,
        ax=axes[1, 1]
    )
    axes[1, 1].axvline(3.0, color='red', linestyle=':', label='BOD Limit (3 mg/L)')
    axes[1, 1].axhline(4.0, color='blue', linestyle=':', label='Min DO Limit (4 mg/L)')
    axes[1, 1].set_title("4. Water Health: Dissolved Oxygen vs Organic Pollution (B.O.D.)", fontsize=13, fontweight='bold')
    axes[1, 1].set_xlabel("B.O.D. (mg/L) - Organic Waste")
    axes[1, 1].set_ylabel("Dissolved Oxygen (mg/L)")
    axes[1, 1].legend(bbox_to_anchor=(1.02, 1), loc='upper left')

    plt.tight_layout()
    output_image = "project_dashboard.png"
    plt.savefig(output_image, dpi=300)
    print(f"[Done] Multi-panel visualization saved as '{output_image}'!")
    plt.show()

if __name__ == "__main__":
    generate_visualizations()