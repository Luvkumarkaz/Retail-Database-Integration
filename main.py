import os
from pipeline.extract import extract_postgres_transactions, extract_mongo_telemetry
from pipeline.transform import clean_and_merge
from pipeline.eda_analysis import run_hypothesis_tests

def main():
    print("========================================")
    print(" Starting Data Integration Pipeline")
    print("========================================")
    
    # 1. Extraction Phase
    df_sql = extract_postgres_transactions()
    df_mongo = extract_mongo_telemetry()
    
    # 2. Transformation Phase
    df_final = clean_and_merge(df_sql, df_mongo)
    
    # 3. Load / Export Phase
    if not df_final.empty:
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/unified_dataset.csv"
        
        df_final.to_csv(output_path, index=False)
        print(f"\n[Pipeline Complete] Data exported successfully to: {output_path}")
        
        # 4. Analysis Phase
        run_hypothesis_tests(df_final)
    else:
        print("\n[Pipeline Failed] No final dataset generated.")

if __name__ == "__main__":
    main()
