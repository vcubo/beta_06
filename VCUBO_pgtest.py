import streamlit as st
import psycopg2

# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

@st.cache(ttl=600)
def run_query_gen(query):
    with conn.cursor() as cur:
        cur.execute(query)

query2 = "CREATE TABLE IF NOT EXISTS mytable2 (name varchar(80), pet varchar(80));"
query3 = "INSERT INTO mytable2 VALUES ('Mary', 'cat'), ('John', 'cat'), ('Robert', 'bird');"
query4 = "INSERT INTO mytable2 VALUES ('Mary', 'cow'), ('John', 'cat'), ('Robert', 'bird');"
run_query_gen(query2)
run_query_gen(query3)
run_query_gen(query4)

rows = run_query("SELECT * from mytable2;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
