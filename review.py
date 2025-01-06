import openai
import pandas as pd

# Your OpenAI API key
openai.api_key = 'your-api-key'

# Read the Excel file using pandas
excel_file = 'venture_capital_data.xlsx'  # Replace with the path to your Excel file
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

# Create two new columns for the reason and status
df['Reason'] = None
df['Status'] = None

# Function to send data to GPT-4 and get response
def get_vc_analysis(data_row):
    prompt = f"""
    Analyze the following venture capital firm information and provide a reason and status about whether it's a good fit for a startup looking for funding:
    Rules:
        include Seed Stage
        invested before 3M - 5M
        should related Invest Al, EdTech

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

    # Send the data to GPT-4 for analysis
    response = openai.Completion.create(
        engine="gpt-4",  # Or use "gpt-3.5-turbo" for faster responses
        prompt=prompt,
        max_tokens=300,  # Adjust token limit based on response length
        temperature=0.7  # Control randomness in response
    )

    # Extract the response text
    response_text = response['choices'][0]['text'].strip()
    
    # Split response into reason and status (you can adjust based on how GPT responds)
    reason, status = response_text.split('\n', 1)
    
    return reason, status

# Loop through each row and send the relevant data to GPT-4
for index, row in df.iterrows():
    reason, status = get_vc_analysis(row)
    df.at[index, 'Reason'] = reason
    df.at[index, 'Status'] = status

# Save the updated dataframe back to an Excel file with the reason and status columns
df.to_excel('updated_venture_capital_data.xlsx', index=False)

print("Analysis complete. Results saved to 'updated_venture_capital_data.xlsx'")
