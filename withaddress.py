import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Selenium WebDriver (Chrome in this case)
options = Options()
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.headless = False  # Disable headless mode
options.add_argument("--no-sandbox")  # Disable sandboxing for better compatibility
options.add_argument("--log-level=3")  # Log only critical messages (errors)
options.add_argument("--disable-logging")  # Disable browser logs
options.add_argument("--enable-unsafe-swiftshader")  # Enable software WebGL fallback
options.add_argument("--allow-insecure-localhost")
options.add_argument('ignore-certificate-errors')
options.add_argument("--disable-web-security")
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
]

# Randomly select a user-agent
user_agent = random.choice(user_agents)
options.add_argument(f"user-agent={user_agent}")

options = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://cacert.org/')

# Function to extract address from href link
def extract_address(href):
    try:
        # Directly use the href (since it's complete)
        url = href
        print(f"Accessing: {url}")
        driver.get(url)

        # Wait for the address element to load (using WebDriverWait to ensure the page is fully loaded)
        # WebDriverWait(driver, 25).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, "//a[contains(@class, 'dt-hd link-to-more olnk') and @data-link-to-more='address']"))
        # )
        time.sleep(15)
        # Extract address from the spans in the specified XPath
        address_parts = driver.find_elements(By.XPATH,
                                             "//a[contains(@class, 'dt-hd link-to-more olnk') and @data-link-to-more='address']")

        # Join the text parts of the address
        address = " ".join([part.text for part in address_parts])

        # If no address is found
        if not address:
            print(f"No address found for {href}")
            return "Address not found"

        return address
    except Exception as e:
        print(f"Error while extracting address from {href}: {e}")
        return "Error extracting address"


# Open the CSV file to read href links
with open('search_results.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)

    # Skip the header row
    next(reader)

    # Open the CSV file for writing the updated information
    with open('search_results_with_addresses.csv', mode='w', newline='', encoding='utf-8') as write_file:
        writer = csv.writer(write_file)
        # Write the header row for the new CSV
        writer.writerow(["Name", "Href", "Address"])

        # Loop through the CSV rows to access each href and extract the address
        for row in reader:
            name = row[0]
            href = row[1]
            if href != "No link found":  # If a valid href is present
                address = extract_address(href)
                # Write the name, href, and extracted address to the new CSV
                writer.writerow([name, href, address])
            else:
                # Write the name, href (No link), and a placeholder for the address
                writer.writerow([name, href, "No address found"])

# Close the driver after use
driver.quit()

print("The addresses have been extracted and written to 'search_results_with_addresses.csv'.")
