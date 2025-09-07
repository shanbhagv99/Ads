import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load campaign data
df = pd.read_csv("Data/marketing_campaign_dataset.csv")

st.title("Ads.AI - Campaign Analyzer")
st.dataframe(df)

df['Acquisition_Cost'] = (
    df['Acquisition_Cost']
    .astype(str)
    .replace('[\$,]', '', regex=True)
    .astype(float)
)

# Summarize by company & channel
df['Conversions'] = df['Clicks'] * df['Conversion_Rate']
summary = df.groupby(['Company', 'Channel_Used']).agg({
    'Clicks': 'sum',
    'Impressions': 'sum',
    'Conversions': 'sum',
    'Acquisition_Cost': 'sum',
    'ROI': 'mean'
}).reset_index()

st.subheader("Campaign Summary")
st.dataframe(summary)

# GPT analysis button
if st.button("Generate AI Analysis"):
    limited_summary = summary.head(20)   # only first 20 rows
    prompt = f"""
    Here is a summarized campaign performance dataset:\n{limited_summary.to_string(index=False)}\n
    Analyze which channels perform best/worst and suggest budget reallocations.
    Be concise.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a marketing strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    st.subheader("AI Insights")
    st.write(response.choices[0].message.content)
