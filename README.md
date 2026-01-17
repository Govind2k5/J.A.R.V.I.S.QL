# J.A.R.V.I.S.QL

**Just A Rather Very Intelligent System for Querying Logic**

A Python application that allows you to query MySQL databases using natural language. It uses the Groq API (Llama 3) to convert English questions into SQL queries.

---

## Features

-   **Natural Language Queries**: Type questions in plain English to get data.
-   **Safe Execution**: 
    -   Read-only mode (blocks `DROP`, `DELETE`, etc.).
    -   Restricted scope (ignores internal system tables).
-   **Fast**: Uses Groq for quick AI responses.
-   **Web UI**: Simple interface built with Streamlit.

---

## Tech Stack

-   **Frontend**: Streamlit
-   **Backend**: Python
-   **Database**: MySQL
-   **AI Model**: Llama 3 (via Groq API)

---

## Setup & Installation

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/Govind2k5/J.A.R.V.I.S.QL.git
    cd J.A.R.V.I.S.QL
    ```

2.  **Install requirements**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure `.env` file**:
    Create a file named `.env` and add your keys:
    ```env
    GROQ_API_KEY=your_key_here
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=your_db
    ```

4.  **Run the app**:
    ```bash
    streamlit run app.py
    ```

---

## How It Works

1.  The app reads your database schema (table names and columns).
2.  It sends your question + the schema to the AI.
3.  The AI generates a SQL query.
4.  The app validates the query (checks for harmful keywords).
5.  If safe, it runs the query and shows the results.

---
