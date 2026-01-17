import os
import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question, schema):
    # get today's date for relative time queries
    today = datetime.date.today()
    
    prompt = f"""
    You are an expert Senior SQL Data Analyst. Your job is to answer complex questions by generating efficient, valid MySQL queries.

    ### Database Schema:
    {schema}

    ### Context:
    - Today's Date: {today} (Use this for relative date calculations like 'last month')

    ### Critical Rules:
    1. **Output**: Return ONLY the raw SQL. No markdown, no explanations.
    2. **Safety**: 
       - generate **READ-ONLY** queries. 
       - **NEVER** generate `DROP`, `DELETE`, `INSERT`, `UPDATE`, or `ALTER` statements.
       - If the user asks to modify data, return `SELECT 'I cannot modify the database'`.
       - **NEVER** query system tables (`information_schema`, `mysql`, `performance_schema`, `sys`). Only use tables listed in 'Database Schema'.
    3. **Logic**:
       - Use **CTEs** (Common Table Expressions) to break down complex logic.
       - Use **Window Functions** (RANK(), ROW_NUMBER(), LAG()) for analytics like "top N per group" or "growth constraints".
       - Determine JOINs dynamically based on foreign keys or naming conventions.
    4. **Robustness**:
       - Handle potential NULL values using `COALESCE(column, 0)` for aggregations.
       - Ensure unambiguous column references (always alias tables, e.g., `e.salary`, `p.name`).
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt}, #tells the llm how to behave
            {"role": "user", "content": question} # what the human asks
        ],
        model="llama-3.1-8b-instant",
    )
    
    return response.choices[0].message.content.strip()
