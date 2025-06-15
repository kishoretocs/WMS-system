
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from openrouter_llm import OpenRouterLLM

st.set_page_config(page_title="Chat with CSV", layout="wide")

st.title("📊 Chat with your CSV using DeepSeek (OpenRouter)")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("✅ CSV Data Preview", df.head())

    # Connect to OpenRouter
    llm = OpenRouterLLM(
        api_key="sk",  # Replace with your actual OpenRouter key
        model="deepseek/deepseek-r1-0528:free"
    )

    sdf = SmartDataframe(df, config={"llm": llm})

    query = st.text_input("💬 Ask a question about your data:")

    if st.button("Run Query") and query:
        try:
            result = sdf.chat(query)
            st.success("✅ Response")
            if isinstance(result, pd.DataFrame):
                st.write(result)
                st.bar_chart(result)
            else:
                st.write(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("Please upload a CSV file to begin.")
