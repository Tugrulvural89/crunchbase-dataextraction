import openpyxl
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import os

# Access variables
USER_PROFILE_GOOGLE_PATH = os.getenv("USER_PROFILE_GOOGLE_PATH")

# Chrome seçeneklerini ayarlayın
options = webdriver.ChromeOptions()
#options.binary_location = "../Downloads/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

#use your google profile
user_data_dir="user-data-dir=" + USER_PROFILE_GOOGLE_PATH
#options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
options.add_argument(user_data_dir) 
# WebDriver örneğini oluşturun
driver = webdriver.Chrome(options=options)

# Load the workbook and sheet (optional, if you want to use openpyxl for some reason)
# workbook = openpyxl.load_workbook("/Users/kasimtugrulvural/Downloads/vc_qualifications.xlsx")
# sheet = workbook.active

# Define a function to scrape data
def scrape_crunchbase_data(org_url):
    try:
        # Use Selenium to load the page with JavaScript rendering
        driver.get(org_url)
        time.sleep(6)  # Allow some time for the page to load completely


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for additional content to load
        
        # Get the page source after JavaScript execution
        html_content = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract required data using BeautifulSoup
        data = {
            "Funds": None,
            "Investments": None,
            "Diversity Investments": None,
            "Exits": None,
            "Investment Stage": None,
            "Recent News": None,
            "Location": None,
            "Employee Count": None,
            "Firm Type": None,
            "Investment Stages": None,
            "Website": None,
            "Rank": None,
            "Phone": None,
            "Contact": None,
            "Description Card": None,
            "Total Investments": None,
        }


        try:
            location_element = soup.select_one('fields-card identifier-multi-formatter span a')
            if location_element:
                data["Location"] = location_element.get_text(strip=True)
            else:
                data["Location"] = "N/A"
        except Exception:
            data["Location"] = "N/A"

        try:
            employee_count_element = soup.select_one('fields-card ul li:nth-child(2) a')
            if employee_count_element:
                data["Employee Count"] = employee_count_element.get_text(strip=True)
            else:
                data["Employee Count"] = "N/A"
        except Exception:
            data["Employee Count"] = "N/A"

        try:
            firm_type_element = soup.select_one('fields-card ul li:nth-child(3) span.component--field-formatter')
            if firm_type_element:
                data["Firm Type"] = firm_type_element.get_text(strip=True)
            else:
                data["Firm Type"] = "N/A"
        except Exception:
            data["Firm Type"] = "N/A"

        try:
            investment_stages_element = soup.select_one('fields-card ul li:nth-child(4) span.component--field-formatter')
            if investment_stages_element:
                data["Investment Stages"] = investment_stages_element.get_text(strip=True)
            else:
                data["Investment Stages"] = "N/A"
        except Exception:
            data["Investment Stages"] = "N/A"

        try:
            website_element = soup.select_one('fields-card ul li:nth-child(5) a')
            if website_element:
                data["Website"] = website_element.get_text(strip=True)
            else:
                data["Website"] = "N/A"
        except Exception:
            data["Website"] = "N/A"

        try:
            rank_element = soup.select_one('fields-card ul li:nth-child(6) a')
            if rank_element:
                data["Rank"] = rank_element.get_text(strip=True)
            else:
                data["Rank"] = "N/A"
        except Exception:
            data["Rank"] = "N/A"

        # Scrape data based on provided CSS selectors
        try:
            funds_element = soup.select_one("#mat-tab-nav-panel-0 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(2) > profile-section > section-card > mat-card > div.section-content-wrapper > anchored-values > div:nth-child(1) > a > div > field-formatter > span")
            if funds_element:
                data["Funds"] = funds_element.get_text(strip=True)
            else:
                data["Funds"] = "N/A"
        except Exception:
            data["Funds"] = "N/A"

        try:
            investments_element = soup.select_one("#mat-tab-nav-panel-0 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(2) > profile-section > section-card > mat-card > div.section-content-wrapper > anchored-values > div:nth-child(2) > a > div > field-formatter > span")
            if investments_element:
                data["Investments"] = investments_element.get_text(strip=True)
            else:
                data["Investments"] = "N/A"
        except Exception:
            data["Investments"] = "N/A"

        try:
            diversity_investments_element = soup.select_one("#mat-tab-nav-panel-0 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(2) > profile-section > section-card > mat-card > div.section-content-wrapper > anchored-values > div:nth-child(3) > a > div > field-formatter > span")
            if diversity_investments_element:
                data["Diversity Investments"] = diversity_investments_element.get_text(strip=True)
            else:
                data["Diversity Investments"] = "N/A"
        except Exception:
            data["Diversity Investments"] = "N/A"

        try:
            exits_element = soup.select_one("#mat-tab-nav-panel-0 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(2) > profile-section > section-card > mat-card > div.section-content-wrapper > anchored-values > div:nth-child(4) > a > div > field-formatter > span")
            if exits_element:
                data["Exits"] = exits_element.get_text(strip=True)
            else:
                data["Exits"] = "N/A"
        except Exception:
            data["Exits"] = "N/A"

        try:
            contanct_element = soup.select_one("div.main-content > row-card:nth-child(2) > profile-section > section-card > mat-card > div.section-content-wrapper > fields-card:nth-child(3) > ul > li:nth-child(1) > field-formatter > blob-formatter > span")
            if contanct_element:
                data["Contact"] = contanct_element.get_text(strip=True)
            else:
                data["Contact"] = "N/A"
        except:
            data["Contact"] = "N/A"

        try:
            phone_path = soup.select_one("div.main-content > row-card:nth-child(2) > profile-section > section-card > mat-card > div.section-content-wrapper > fields-card:nth-child(3) > ul > li:nth-child(2) > field-formatter > blob-formatter > span")
            if phone_path:
                data["Phone"] = phone_path.get_text(strip=True)
            else:
                data["Phone"] = "N/A"
        except:
            data["Phone"] = "N/A"

        try:
            investment_stage_element = soup.select_one("#mat-tab-nav-panel-8 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(1) > profile-section > section-card > mat-card > div.section-content-wrapper > fields-card:nth-child(3) > ul > li:nth-child(4) > label-with-icon > span > field-formatter > enum-multi-formatter > span")
            if investment_stage_element:
                data["Investment Stage"] = investment_stage_element.get_text(strip=True)
            else:
                data["Investment Stage"] = "N/A"
        except Exception:
            data["Investment Stage"] = "N/A"

        try:
            #mat-tab-nav-panel-8 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(3) > profile-section > section-card > mat-card > div.section-content-wrapper > inline-timeline-card > div:nth-child(1) > div.activity-details > press-reference
            # "Recent News" verisini çekin
            try:
                funding_rounds = soup.find_all("funding-round")  # Tüm funding-round tag'lerini bulun
                texts = ' '.join([tag.get_text(strip=True) for tag in funding_rounds])  # Her tag'in metnini alın
                if texts:
                    data["Recent News"] = texts
                else:
                    data["Recent News"] = "N/A"
            except Exception:
                data["Recent News"] = "N/A"
        except Exception as e:
            print(f"Error Signals & News tab: {e}")
            data["Recent News"] = "N/A"

        try:
            #mat-tab-nav-panel-8 > div > full-profile > page-centered-layout.overview-divider.ng-star-inserted > div > row-card > div > div:nth-child(3) > profile-section > section-card > mat-card > div.section-content-wrapper > inline-timeline-card > div:nth-child(1) > div.activity-details > press-reference
            # "Recent News" verisini çekin
            try:
                description_card = soup.find_all("description-card")  # Tüm funding-round tag'lerini bulun
                texts = ' '.join([tag.get_text(strip=True) for tag in description_card])  # Her tag'in metnini alın
                if texts:
                    data["Description Card"] = texts
                else:
                    data["Description Card"] = "N/A"
            except Exception:
                data["Description Card"] = "N/A"

        except Exception as e:
            print(f"Error Description Card: {e}")
            data["Description Card"] = "N/A"


        try:


            
            new_url = org_url + "/recent_investments"
            driver.get(new_url)
            time.sleep(2)  # Allow some time for the page to load completely


            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for additional content to load
            

            # Find the table that contains the data
            table = driver.find_element(By.CSS_SELECTOR, "#mat-tab-nav-panel-0 > div > full-profile > page-centered-layout.content-cards > div > div > div.main-content > row-card:nth-child(1) > profile-section > section-card > mat-card > div.section-content-wrapper > list-card > div > table")
            
            # Find all rows in the table's body (tbody)
            rows = table.find_elements(By.CSS_SELECTOR, "tbody > tr")
            
            total_price = 0  # Initialize a variable to sum the prices
            
            # Loop through each row and extract the price from the 5th column (td:nth-child(5))
            for row in rows:
                price_cell = row.find_elements(By.CSS_SELECTOR, "td:nth-child(5)")
                
                # Make sure there's a price in the 5th column
                if price_cell:
                    price_text = price_cell[0].text
                    
                    # Clean the price text by removing the dollar sign and any spaces
                    price_text_clean = price_text.replace('$', '').replace('M', '').replace('K', '').strip()
                    
                    # Convert the cleaned price to float and add it to the total
                    try:
                        price = float(price_text_clean)
                        total_price += price
                    except ValueError:
                        print(f"Skipping invalid price: {price_text_clean}")
            data["Total Investments"] = str(total_price)

        except:
            data["Total Investments"] = "N/A"

        return data

    except Exception as e:
        print(f"Error scraping data for {org_url}: {e}")
        return {
            "Funds": "N/A",
            "Investments": "N/A",
            "Diversity Investments": "N/A",
            "Exits": "N/A",
            "Investment Stage": "N/A",
            "Recent News": "N/A",
            "Location": "N/A",
            "Employee Count": "N/A",
            "Firm Type": "N/A",
            "Investment Stages": "N/A",
            "Website": "N/A",
            "Rank": "N/A",
            "Phone": "N/A",
            "Contact": "N/A",
            "Description Card": "N/A",
            "Total Investments": "N/A",
        }

# Read the Excel file with pandas
file_path = "./vc_qualificationsd.xlsx"
df = pd.read_excel(file_path)


new_columns = {
    "Funds": "Funds",
    "Investments": "Investments",
    "Diversity Investments": "Diversity Investments",
    "Exits": "Exits",
    "Investment Stage": "Investment Stage",
    "Recent News": "Recent News",
    "Location": "Location",
    "Employee Count": "Employee Count",
    "Firm Type": "Firm Type",
    "Investment Stages": "Investment Stages",
    "Website": "Website",
    "Rank": "Rank",
    "Contact": "Contact",
    "Phone": "Phone",
    "Description Card": "Description Card",
    "Total Investments": "Total Investments",
}

# Yeni sütunları DataFrame'e ekleyin
for col_name in new_columns.values():
    df[col_name] = None

# Loop through each row, scrape data, and update the DataFrame
for index, row in df.iterrows():
    org_url = row['Crunchbase']  # Assuming the Crunchbase URL is in the 'Crunchbase' column
    print(f"Scraping data for {org_url}...")

     # Scrape the Crunchbase data
    scraped_data = scrape_crunchbase_data(org_url)


        # Check the structure of scraped_data before assignment
    for key, col_name in new_columns.items():
        value = scraped_data.get(key, "N/A")  # Default to "N/A" if key is missing
        print(f"Assigning {col_name}: {value}")  # Debugging print statement
        df.loc[index, col_name] = value  # Ensure single value assignment

    
    # Optional: Save intermediate results every 10 organizations
   
    df.to_excel("updated_vc_qualifications.xlsx", index=False)
    print(f"Intermediate results saved for {index + 1} organizations.")

# Save the updated DataFrame back to the Excel file
updated_file_path = "./updated_vc_qualifications.xlsx"
df.to_excel(updated_file_path, index=False)

print(f"Data scraping completed. Updated file saved to: {updated_file_path}")

# Close the WebDriver
driver.quit()
