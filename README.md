# Leya AI Operations Specialist Case Task - Venture Capital Qualification for Bold

This project outlines an automated and scalable approach to identifying suitable Venture Capital (VC) firms for Bold's Seed fundraising round. The solution employs web scraping, data analysis, and GPT-4 integration to streamline the qualification process, ensuring accuracy despite potential data inconsistencies in the provided Crunchbase list.

## Deliverable 1: Venture Capital Qualification Criteria

### "Fit" Criteria:

-   **Investment Stage:** Includes Seed stage investments.
-   **Investment Focus:** Prioritizes AI, EdTech, or Consumer applications.
-   **Investment History:** Preference for Seed investments in the $3M-$5M range.
-   **Location:** A global outlook or presence in key markets is preferred.

### "Not Fit" Criteria:

-   **Investment Stage:** Focus exclusively on Series A or later stages.
-   **Investment Focus:** No history of investing in AI, EdTech, or related sectors.
-   **Geographic Restrictions:** Limited to regions excluding Bold's target markets.

### Reasoning:

-   Criteria are aligned with Bold's current fundraising needs.
-   Data is extracted primarily from sections like "Investment Stages," "Portfolio," and "About Us" on VC websites.

## Deliverable 2: Proof of Concept (PoC)

### Automation Tools:

-   **Selenium:** Automates web browsing and handles dynamic website content.
-   **Beautiful Soup:** Parses HTML for efficient data extraction.
-   **Openpyxl and Pandas:** Handles Excel data manipulation.
-   **GPT-4 (via OpenAI API):** Analyzes extracted data for classification.

### PoC Process:

1.  **Data Extraction:**
    -   A Selenium script navigates VC websites and extracts relevant data such as investment stage, focus, and recent investments.
    -   Extracted data is stored in a structured format.

2.  **Data Enhancement:**
    -   The data is enriched with additional columns such as "Reason" and "Status" in the spreadsheet.

3.  **GPT-4 Integration:**
    -   Data is sent to GPT-4 using the OpenAI API with predefined rules for analysis.
    -   GPT-4 outputs "Reason" and "Status" (e.g., "Fit" or "Not Fit").

4.  **Validation:**
    -   Results from the automated process were validated against a manually checked batch of 20 VCs, achieving 95% accuracy.

## Deliverable 3: Scaling Up and Prioritization

### Scaling Up:

The developed PoC was applied to the full list of 300+ VCs.

### Prioritization Framework:

-   **Tier 1 (High Priority):** Strong focus on AI/EdTech, Seed investments in the $3M-$5M range, and positive GPT-4 analysis.
-   **Tier 2 (Medium Priority):** Meet some "Fit" criteria but have less relevant investment history or sector focus.
-   **Tier 3 (Low Priority):** Show potential but don’t strongly align with the "Fit" criteria.

### Ranking within Tiers:

-   Recency of investments in relevant sectors.
-   Fund size and investment capacity.
-   Positive sentiment in GPT-4 analysis.

## Setup and Installation Guide

1.  **Clone the Repository:**

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Install Required Dependencies:**

    Make sure you have Python installed on your system.

    ```bash
    pip install -r requirements.txt
    ```

3.  **OpenAI API Integration:**

    -   Obtain an API key from OpenAI.
    -   Add your API key to the environment variables or a `.env` file in the following format:

    ```
    OPENAI_API_KEY=<your-api-key>
    ```

    -   Ensure the script uses the OpenAI GPT-4 API to process the extracted data.

4.  **Selenium Setup:**

    -   Download ChromeDriver: [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
    -   Add ChromeDriver to PATH: Place the downloaded file in a folder and add its path to your system's environment variables.

4.  **Run the Script:**

    -  Run first scrapy wait until the browser is ready: ```python scrapy.py ```
    -  Run main script: ```python review.py ```
    