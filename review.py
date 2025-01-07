import os
import openai
import pandas as pd
import time

# Your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Get API key from environment variable

# Read the Excel file using pandas
excel_file = './venture_capital_data.xlsx'
df = pd.read_excel(excel_file)

# Define the columns you want to send to GPT-4
columns_to_send = [
    'Investment Stage',
    'Industries',
    'Funds',
    'Investments',
    'Diversity Investments',
    'Exits',
    'Recent News',
    'Location',
    'Employee Count',
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
    Analyze the following venture capital firm information and provide a reason and status about whether it's a good fit for a startup looking for funding:
    Rules:
        - Should be in the Seed Stage
        - Invested between 3M $ and 5M $
        - Should be related to AI or EdTech

    Investment Stage: {data_row['Investment Stage']}
    Industries: {data_row['Industries']}
    Funds: {data_row['Funds']}
    Investments: {data_row['Investments']}
    Diversity Investments: {data_row['Diversity Investments']}
    Exits: {data_row['Exits']}
    Recent News: {data_row['Recent News']}
    Location: {data_row['Location']}
    Employee Count: {data_row['Employee Count']}
    Firm Type: {data_row['Firm Type']}
    Investment Stages: {data_row['Investment Stages']}
    Website: {data_row['Website']}
    Rank: {data_row['Rank']}
    Contact: {data_row['Contact']}
    Phone: {data_row['Phone']}
    Description Card: {data_row['Description Card']}

    Based on the provided details, determine if this VC firm would be a good fit for a seed-stage technology startup, focusing on AI or EdTech. Provide a reason and status.
    """

    try:
        # Send the data to GPT-4 for analysis
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.5
        )

        # Extract the response text
        response_text = response.choices[0].message.content.strip()

        # Split response into reason and status (try-catch for flexibility)
        response_lines = response_text.split('\n')
        reason = response_lines[0] if len(response_lines) > 0 else "No reason provided"
        status = response_lines[1] if len(response_lines) > 1 else "Unknown"

        return reason, status
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

