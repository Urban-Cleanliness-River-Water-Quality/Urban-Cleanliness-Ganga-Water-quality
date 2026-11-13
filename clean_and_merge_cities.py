import pandas as pd
import numpy as np

def clean_and_merge_cities():
    print("[1/3] Loading city datasets...")
    df_3m = pd.read_csv("Three million plus city data uncleaned.csv")
    df_3l_1m = pd.read_csv("Three Lakhs to 1 million uncleand dataset.csv")

    # Add category labels
    df_3m['population_category'] = '> 3 Million'
    df_3l_1m['population_category'] = '3 Lakh - 1 Million'

    # Standardize column names
    standard_columns = [
        'source_id', 'category_rank', 'state_ut', 'ulb_name',
        'total_score', 'ss2024_score', 'gfc_star_rating_score', 'odf_score', 'population_category'
    ]
    df_3m.columns = standard_columns
    df_3l_1m.columns = standard_columns

    # Concatenate both into one master city dataset
    combined_df = pd.concat([df_3m, df_3l_1m], ignore_index=True)

    # 1. Clean State text
    combined_df['state_ut'] = combined_df['state_ut'].astype(str).str.title().str.strip()

    # 2. Clean City / ULB Name
    combined_df['city_clean'] = (
        combined_df['ulb_name']
        .astype(str)
        .str.replace(r"\s*\(M\.\s*Corp\)", "", regex=True)
        .str.replace(r"\s*\(MC\)", "", regex=True)
        .str.title()
        .str.strip()
    )

    # 3. Compute overall combined rank (sorted by total_score descending)
    combined_df = combined_df.sort_values(by='total_score', ascending=False).reset_index(drop=True)
    combined_df['overall_rank'] = combined_df.index + 1

    # Reorder columns cleanly
    final_cols = [
        'overall_rank', 'category_rank', 'population_category',
        'city_clean', 'state_ut', 'total_score',
        'ss2024_score', 'gfc_star_rating_score', 'odf_score'
    ]
    combined_df = combined_df[final_cols]

    output_file = "combined_city_clean.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"[Done] Merged {len(combined_df)} cities saved to '{output_file}'!")

if __name__ == "__main__":
    clean_and_merge_cities()