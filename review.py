import os
from openai import OpenAI
import pandas as pd
import time

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Read the Excel file using pandas
excel_file = './updated_vc_qualifications.xlsx'
df = pd.read_excel(excel_file)

# Define the columns you want to send to GPT-4
columns_to_send = [
    'Industries',
    'Funds',
    'Diversity Investments',
    'Exits',
    'Recent News',
    'Location',
    'Firm Type',
    'Investment Stages',
    'Website',
    'Rank',
    'Contact',
    'Phone',
    'Description Card'
]

# Check if all required columns are in the dataframe
missing_columns = [col for col in columns_to_send if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns in Excel file: {missing_columns}")

# Create two new columns for the reason and status
df['Reason'] = None
df['Status'] = None

# Function to send data to GPT-4 and get response
def get_vc_analysis(data_row):
    # Prepare the prompt
    prompt = f"""
    Analyze the following venture capital firm information and determine if it's a good fit for a startup looking for funding:
    Rules:
        - Should be in the Seed Stage
        - Invested between 3M $ and 5M $
        - Should be related to AI or EdTech

    Provide a detailed reason explaining why it is a fit or not, and a status ("Fit" or "Not Fit") based on the criteria.

    Industries: {data_row['Industries']}
    Funds: {data_row['Funds']}
    Diversity Investments: {data_row['Diversity Investments']}
    Exits: {data_row['Exits']}
    Recent News: {data_row['Recent News']}
    Location: {data_row['Location']}
    Firm Type: {data_row['Firm Type']}
    Investment Stages: {data_row['Investment Stages']}
    Website: {data_row['Website']}
    Rank: {data_row['Rank']}
    Contact: {data_row['Contact']}
    Phone: {data_row['Phone']}
    Description Card: {data_row['Description Card']}

    Return the output in the format:
    - Reason: [Detailed explanation]
    - Status: [Fit or Not Fit]
    """

    try:
        # Send the data to GPT-4 for analysis
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.5
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Parse the response
        reason_line = response_text.split('- Reason: ')[1].split('- Status: ')[0].strip()
        status_line = response_text.split('- Status: ')[1].strip()

        # Ensure status is "Fit" or "Not Fit"
        if status_line not in ["Fit", "Not Fit"]:
            raise ValueError(f"Invalid status received: {status_line}")

        return reason_line, status_line
    except Exception as e:
        return f"Error during analysis: {e}", "Error"

# Loop through each row and send the relevant data to GPT-4
for index, row in df.iterrows():
    print(f"Processing row {index + 1}/{len(df)}...")
    try:
        reason, status = get_vc_analysis(row)
        df.at[index, 'Reason'] = reason
        df.at[index, 'Status'] = status
    except Exception as e:
        df.at[index, 'Reason'] = "Error"
        df.at[index, 'Status'] = f"Error: {e}"
    time.sleep(1)  # Delay to avoid rate limits (adjust as needed)

# Save the updated dataframe back to an Excel file
output_file = 'updated_venture_capital_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Analysis complete. Results saved to '{output_file}'")
