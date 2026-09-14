import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient
from .config import PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, PG_DB, MONGO_URI, MONGO_DB

def extract_postgres_transactions():
    """Extracts structured transaction data from PostgreSQL."""
    conn_str = f"host={PG_HOST} port={PG_PORT} dbname={PG_DB} user={PG_USER} password={PG_PASSWORD}"
    query = """
        SELECT t.transaction_id, t.user_id, t.product_id, t.amount as total_revenue, 
               p.category, u.signup_date
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
        JOIN users u ON t.user_id = u.user_id;
    """
    try:
        with psycopg2.connect(conn_str) as conn:
            df = pd.read_sql_query(query, conn)
        print(f"[Extract] {len(df)} rows pulled from PostgreSQL.")
        return df
    except Exception as e:
        print(f"[Extract Error] PostgreSQL: {e}")
        return pd.DataFrame()

def extract_mongo_telemetry():
    """Extracts unstructured telemetry and reviews from MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        
        # Extract telemetry
        telemetry_data = list(db.telemetry.find({}, {"_id": 0}))
        df_telemetry = pd.DataFrame(telemetry_data)
        
        # Extract reviews
        reviews_data = list(db.reviews.find({}, {"_id": 0}))
        df_reviews = pd.DataFrame(reviews_data)
        
        # Flatten and merge NoSQL data internally before SQL merge
        if not df_reviews.empty and not df_telemetry.empty:
            df_mongo = pd.merge(df_telemetry, df_reviews, on=['user_id', 'product_id'], how='left')
        else:
            df_mongo = df_telemetry
            
        print(f"[Extract] {len(df_mongo)} rows pulled from MongoDB.")
        return df_mongo
    except Exception as e:
        print(f"[Extract Error] MongoDB: {e}")
        return pd.DataFrame()
