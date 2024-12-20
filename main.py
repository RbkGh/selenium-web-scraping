import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# List of names to search
names_list = ['Agyemang']
# names_list = ['Agyemang', 'Addo', 'Kofi']

# Set up the Selenium WebDriver (Chrome in this case)
options = Options()
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.headless = False  # Disable headless mode
options.add_argument("--no-sandbox")  # Disable sandboxing for better compatibility
options.add_argument("--log-level=3")  # Log only critical messages (errors)
options.add_argument("--disable-logging")  # Disable browser logs
options.add_argument("--enable-unsafe-swiftshader")  # Enable software WebGL fallback
options.add_argument("--allow-insecure-localhost")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Function to search for a name on TruePeopleSearch.com using the direct URL
def search_truepeople(name):
    # Construct the search URL by appending the name
    url = f"https://www.truepeoplesearch.com/results?name={name}&citystatezip=Massachusetts"

    # Open the constructed URL
    driver.get(url)

    # Wait for the page to load and the results to appear (use WebDriverWait)
    try:
        # Wait until the div with class 'col-md-8' (where the name is) and 'col-md-4' (where the href is) are loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'col-md-8')]//div[contains(@class, 'h4')]"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//div[contains(@class, 'col-md-4 hidden-mobile text-center align-self-center')]//a[@class='btn btn-success btn-lg detail-link shadow-form']"))
        )

        # Extract names from the div with class 'col-md-8' and 'h4' tags inside it
        names = [name_element.text for name_element in
                 driver.find_elements(By.XPATH, "//div[contains(@class, 'col-md-8')]//div[contains(@class, 'h4')]")]

        # Extract href values from the specified div
        hrefs = [link.get_attribute('href') for link in driver.find_elements(By.XPATH,
                                                                             "//div[contains(@class, 'col-md-4 hidden-mobile text-center align-self-center')]//a[@class='btn btn-success btn-lg detail-link shadow-form']")]

        return names, hrefs

    except Exception as e:
        print(f"Error while scraping {name}: {e}")
        return [], []


# Open the CSV file for writing
with open('search_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row to the CSV
    writer.writerow(["Name", "Href"])

    # Loop through the names and search for each
    for name in names_list:
        names, hrefs = search_truepeople(name)

        # Ensure the names and hrefs are paired correctly
        for i in range(max(len(names), len(hrefs))):
            name_value = names[i] if i < len(names) else "No name found"
            href_value = hrefs[i] if i < len(hrefs) else "No link found"
            writer.writerow([name_value, href_value])

# Close the driver after use
driver.quit()

print("Search results with names and href values have been written to 'search_results.csv'.")
