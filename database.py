import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_schema():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    schema = []
    for (table_name,) in tables:
        cursor.execute(f"DESCRIBE {table_name}")
        
        columns = []
        for col in cursor.fetchall():
            columns.append(col[0])
            
        schema.append(f"Table: {table_name}\nColumns: {', '.join(columns)}")
        
    conn.close()
    return "\n".join(schema)

def run_query(query):
    # safety check
    forbidden_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE"]
    
    if any(keyword in query.upper() for keyword in forbidden_keywords):
        return None, None, "SAFETY ALERT: Destructive queries are not allowed."

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        
        columns = []
        for desc in cursor.description:
            columns.append(desc[0])
            
        return result, columns, None
    except Exception as e:
        return None, None, str(e)
    finally:
        conn.close()
