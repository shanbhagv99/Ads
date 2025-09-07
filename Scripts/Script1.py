import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Project root is one level up
project_root = os.path.join(script_dir, "..")
dotenv_path = os.path.join(project_root, ".env")

# Load the .env file explicitly
load_dotenv(dotenv_path)

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found! Make sure .env exists and has OPENAI_API_KEY.")

print("API key loaded:", bool(api_key))  # Should print True

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Load campaign data CSV
csv_path = os.path.join(project_root, "Data", "marketing_campaign_dataset.csv")
df = pd.read_csv(csv_path)

# Aggregate data
def compute_group_summary(df, group_field):
    # Calculate conversions as Clicks * Conversion_Rate
    df['Conversions'] = df['Clicks'] * df['Conversion_Rate']
    # Convert Acquisition_Cost to numeric
    df['Acquisition_Cost'] = pd.to_numeric(df['Acquisition_Cost'].replace('[\$,]', '', regex=True))
    # Group and aggregate
    summary = df.groupby(group_field).agg({
        'Clicks': 'sum',
        'Impressions': 'sum',
        'Conversions': 'sum',
        'Acquisition_Cost': 'sum',
        'ROI': 'mean'  # avg ROI per group
    }).reset_index()
    # Calculate derived metrics
    summary['Conversion_Rate'] = summary['Conversions'] / summary['Clicks'].replace(0, 1)
    summary['Cost_per_Acquisition'] = summary['Acquisition_Cost'] / summary['Conversions'].replace(0, 1)
    summary['Impressions_per_Conversion'] = summary['Impressions'] / summary['Conversions'].replace(0, 1)
    return summary

# Summarize by channel
group_fields = ['Company', 'Channel_Used', 'Target_Audience']
full_summary = compute_group_summary(df, group_fields)
full_summary_str = full_summary.to_string(index=False)

# Combine summary
summary = f"Summary by Company, Channel, and Target Audience:\n{full_summary_str}"

# Prepare prompt for GPT
prompt = f"""
You are a marketing AI assistant.
Here is the campaign performance summary:\n{full_summary_str}\n
Analyze which channel is performing best, which company is doing well, which is worst,
and recommend budget reallocation strategies.
Be specific and concise.
"""

# Make GPT request
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a marketing strategist."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.4
)

# Print GPT analysis
print("\nAI Analysis:\n", response.choices[0].message.content)
