import streamlit as st
import requests
import pandas as pd

# Custom Page Title
st.markdown(
    "<h1 style='text-align: center; color: #00AEEF;'>Dilytics Procurement Assistant</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size:16px;'>Welcome to My AI. I am here to help with Dilytics Procurement Insights Solutions</p>",
    unsafe_allow_html=True
)

# Input box
query = st.text_input("Ask a question...")

if st.button("Submit"):
    if query:
        with st.spinner("Thinking..."):
            # SQL Endpoint
            sql_response = requests.post(
                st.secrets["GCP_ENDPOINT_SQL"],
                json={"question": query}
            )
            sql_json = sql_response.json()

            # Chart Endpoint (optional, only if explicitly requested)
            chart_response = requests.post(
                st.secrets["GCP_ENDPOINT_CHART"],
                json={"question": query}
            )
            chart_url = chart_response.json().get("chart_url")

        # User question bubble
        st.markdown(
            f"""
            <div style='background-color:#ffcccc;padding:10px;border-radius:10px;margin-bottom:10px'>
            <strong>🧾 {query}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Final AI answer bubble
        if "answer" in sql_json:
            st.markdown(
                f"""
                <div style='background-color:#fff3cd;padding:10px;border-radius:10px;margin-bottom:10px'>
                <strong>📦 {sql_json['answer']}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Show SQL
        if "sql" in sql_json:
            with st.expander("View SQL Query"):
                st.code(sql_json["sql"], language="sql")

        # Show simplified query results
        data = sql_json.get("data", [])
        if data:
            st.markdown("#### 📊 Query Results:")
            if len(data) == 1 and "rows" in data[0]:
                st.write(f"Rows: {data[0]['rows']}")
            else:
                df = pd.DataFrame(data)
                st.dataframe(df)
        else:
            st.warning("No data found.")

        # Show chart only if explicitly requested (e.g., "show chart")
        if chart_url and "show chart" in query.lower():
            st.image(chart_url, caption="Generated Chart")
    else:
        st.warning("Please enter a question.")
