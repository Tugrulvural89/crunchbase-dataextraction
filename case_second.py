import openpyxl
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI
import traceback

# Access variables
USER_PROFILE_GOOGLE_PATH = os.getenv("USER_PROFILE_GOOGLE_PATH")

# Chrome options
options = webdriver.ChromeOptions()
# Use your Google profile
user_data_dir = "user-data-dir=" + USER_PROFILE_GOOGLE_PATH
options.add_argument(user_data_dir)

# WebDriver instance
driver = webdriver.Chrome(options=options)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to validate scraped content
def validate_data(content):
    return "yes" if content.strip() else "no"

# Function to send text to OpenAI and determine "fit/not fit"
def evaluate_fit(content):
    try:
        # Prepare the prompt for OpenAI GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant trained to evaluate venture capital firms based on specific criteria."},
                {"role": "user", "content": f"Evaluate the following content to determine if it meets the criteria for 'fit' or 'not fit': {content}. "
                                          "Criteria: 1. Focus includes keywords like B2C, consumer-focused, or AI. "
                                          "2. Round types include Seed, Early-stage. Provide 'fit' or 'not fit'."}
            ],
            max_tokens=4000,  # Limit tokens for concise responses
            temperature=0.5
        )

        print(response.choices[0].message.content.strip())
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error evaluating content: {str(e)}")
        print(traceback.format_exc())
        return "error"

# Function to start scraping
def start_scrapy(url):
    try:
        driver.get(url)
        
        # Wait for elements to load instead of using sleep
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p | //li | //h1 | //h2 | //h3"))
        )
        
        elements = driver.find_elements(By.XPATH, "//p | //li | //h1 | //h2 | //h3")
        text_content = " ".join([elem.text for elem in elements])
        return text_content
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

# Main function to process Excel data
def process_excel(file_path):
    try:
        # Read the Excel file with pandas
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Ensure required columns are present
    if "VC Website" not in df.columns:
        print("Error: 'VC Website' column not found in the Excel file.")
        return

    # Add new columns for results
    df["Fit/Not Fit"] = ""
    df["Validated"] = ""

    # Loop through each row and process
    for index, row in df.iterrows():
        url = row["VC Website"]
        if not pd.isna(url):
            print(f"Processing: {url}")
            scraped_content = start_scrapy(url)
            fit_status = evaluate_fit(scraped_content)
            validation_status = validate_data(scraped_content)

            # Update the DataFrame
            df.at[index, "Fit/Not Fit"] = fit_status
            df.at[index, "Validated"] = validation_status
        else:
            print(f"Skipping empty URL at row {index}")

    # Save the updated DataFrame to a new Excel file
    output_file = "updated_vc_data.xlsx"
    try:
        df.to_excel(output_file, index=False)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving updated Excel file: {e}")

# Main execution
if __name__ == "__main__":
    file_path = "./vc_qualificationsd.xlsx"
    process_excel(file_path)
    driver.quit()
