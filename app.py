import streamlit as st
import requests
import pandas as pd

st.title("Welcome to Google AI Chatbot")

query = st.text_input("Ask a question")

if st.button("Submit"):
    if query:
        # Call SQL endpoint
        sql_response = requests.post(
            st.secrets["GCP_ENDPOINT_SQL"],
            json={"question": query}
        )

        st.write("Raw SQL Response:", sql_response.json())
        data = sql_response.json().get("data", [])

        if data:
            st.write("SQL Results:")
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.write("No data found.")

        # Call Chart endpoint
        chart_response = requests.post(
            st.secrets["GCP_ENDPOINT_CHART"],
            json={"question": query}
        )
        chart_url = chart_response.json().get("chart_url")

        if chart_url:
            st.image(chart_url, caption="Generated Chart")
    else:
        st.warning("Please enter a query.")



