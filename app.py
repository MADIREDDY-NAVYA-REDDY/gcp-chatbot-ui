import streamlit as st
import requests
import pandas as pd

# ---- Header UI ----
st.markdown("""
    <h1 style='text-align: center; color: #00AEEF;'>Dilytics Google AI Procurement Assistant</h1>
    <p style='text-align: center;'>Welcome to Google AI. I am here to help with Dilytics Procurement Insights Solutions</p>
    """, unsafe_allow_html=True)

# ---- Text Input ----
query = st.text_input("Ask your question...")

# ---- On Submit ----
if st.button("Submit"):
    if query:
        with st.spinner("Fetching response..."):
            # SQL Response
            sql_response = requests.post(
                st.secrets["GCP_ENDPOINT_SQL"],
                json={"question": query}
            )
            sql_json = sql_response.json()

            # Chart Response
            chart_response = requests.post(
                st.secrets["GCP_ENDPOINT_CHART"],
                json={"question": query}
            )
            chart_url = chart_response.json().get("chart_url")

        # ---- User Question ----
        st.markdown(f"""
            <div style='background-color:#fde2e2;padding:12px 20px;border-radius:15px;margin:10px 0;font-size:16px'>
                <strong>🧾 {query}</strong>
            </div>
        """, unsafe_allow_html=True)

        # ---- Assistant Response ----
        if "answer" in sql_json:
            st.markdown(f"""
                <div style='background-color:#fff8d2;padding:12px 20px;border-radius:15px;margin:10px 0;font-size:16px'>
                    <strong>📦 {sql_json['answer']}</strong>
                </div>
            """, unsafe_allow_html=True)

        # ---- SQL Query Expandable ----
        if "sql" in sql_json:
            with st.expander("View SQL Query"):
                st.code(sql_json["sql"], language="sql")

        # ---- Query Results Table ----
        data = sql_json.get("data", [])
        if data:
            df = pd.DataFrame(data)
            st.markdown("### 📊 Query Results:")
            st.dataframe(df)
        else:
            st.warning("No data found.")

        # ---- Chart Image ----
        if chart_url:
            st.image(chart_url, caption="Generated Chart")
    else:
        st.warning("Please enter a question.")

