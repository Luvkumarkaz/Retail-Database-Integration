import pandas as pd

def clean_and_merge(df_sql, df_mongo):
    """
    Merges SQL transactions with MongoDB telemetry.
    Uses a Left Join to ensure hard business revenue data is never dropped,
    even if web telemetry was blocked or lost.
    """
    if df_sql.empty:
        print("[Transform] SQL DataFrame is empty. Cannot merge.")
        return pd.DataFrame()
        
    if not df_mongo.empty:
        # Left join anchored on the SQL transaction table
        df_merged = pd.merge(df_sql, df_mongo, on='user_id', how='left')
        
        # Feature Engineering: Clean missing telemetry for transactions
        df_merged['session_duration_sec'] = df_merged['session_duration_sec'].fillna(0)
        df_merged['total_clicks'] = df_merged['total_clicks'].fillna(0)
        
        # Determine if a review exists based on rating presence
        if 'rating' in df_merged.columns:
            df_merged['has_review'] = df_merged['rating'].notna()
        else:
            df_merged['has_review'] = False
            
    else:
        print("[Transform] Mongo DataFrame is empty. Proceeding with SQL data only.")
        df_merged = df_sql
        
    print(f"[Transform] Merged dataset generated with {len(df_merged)} rows.")
    return df_merged
