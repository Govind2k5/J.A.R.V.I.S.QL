import streamlit as st
import pandas as pd
import database
import llm

st.set_page_config(page_title="J.A.R.V.I.S.QL", page_icon="🤖", layout="centered")

# sidebar
with st.sidebar:
    st.header("Menu")
    st.caption("Under the hood controls for the curious.")
    
    if st.toggle("Peek at Database Schema 👀"):
        try:
            with st.expander("Schema Definition", expanded=True):
                st.code(database.get_schema(), language="sql")
        except Exception as e:
            st.error(f"DB Error: {e}")
# title
st.title("🤖 J.A.R.V.I.S.QL")
st.caption("Your AI-powered data companion. Just ask.")

query = st.text_input("What would you like to know?", placeholder="e.g., Show me the top 5 projects by budget...")

if st.button("Ask Jarvis 🚀", type="primary") and query:
    with st.spinner("Consulting the oracle... 🔮"):
        try:
            schema = database.get_schema()
            sql_query = llm.generate_sql(query, schema)
            clean_sql = sql_query.replace("```sql", "").replace("```", "").strip() #cleaning the result
            
            with st.expander("See generated SQL code 💻"):
                st.code(clean_sql, language="sql")
            
            data, columns, error = database.run_query(clean_sql)
            
            if error:
                st.error(f"💥 Query Failed: {error}")
            elif data:
                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.warning("No results found.")
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")