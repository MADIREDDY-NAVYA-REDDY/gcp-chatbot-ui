import streamlit as st
import requests
import pandas as pd

# Header
st.markdown("<h1 style='text-align: center; color: #00AEEF;'>Cortex AI-Procurement Assistant by DiLytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Welcome to Cortex AI. I am here to help with Dilytics Procurement Insights Solutions</p>", unsafe_allow_html=True)

# Input box
query = st.text_input("Ask a question")

if st.button("Submit"):
    if query:
        with st.spinner("Thinking..."):
            # Call SQL endpoint
            sql_response = requests.post(
                st.secrets["GCP_ENDPOINT_SQL"],
                json={"question": query}
            )
            sql_data = sql_response.json()

            # Optional chart endpoint
            chart_response = requests.post(
                st.secrets["GCP_ENDPOINT_CHART"],
                json={"question": query}
            )
            chart_url = chart_response.json().get("chart_url")

        # User question bubble
        st.markdown(f"#### 🧾 {query}")

        # Final answer (if available)
        if "answer" in sql_data:
            st.markdown(f"#### 📦 {sql_data['answer']}")

        # SQL query toggle
        if "sql" in sql_data:
            with st.expander("View SQL Query"):
                st.code(sql_data["sql"], language="sql")

        # Data output
        data = sql_data.get("data", [])
        if data:
            st.markdown("#### 📊 Query Results:")
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.warning("No data found.")

        # Chart output
        if chart_url:
            st.image(chart_url, caption="Generated Chart")

    else:
        st.warning("Please enter a query.")

