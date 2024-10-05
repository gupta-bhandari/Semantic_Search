import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Open the browser in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to collect links from the current page
def collect_product_links():
    a_tags = driver.find_elements(By.CSS_SELECTOR, "div.RfADt a")
    links = []
    for a in a_tags:
        href = a.get_attribute('href')
        if href.startswith("//"):
            href = "https:" + href
        links.append(href)
    return links

# Function to extract data from a product page
def extract_product_data(link):
    print(f"Visiting link: {link}")
    driver.get(link)

    # WebDriverWait for elements to load
    product_data = {"link": link, "product_title": "", "price": "", "actual_price": "", "ratings": "", "color": ""}

    try:
        product_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pdp-mod-product-badge-title'))).text
        product_data["product_title"] = product_title

        try:
            price = driver.find_element(By.CSS_SELECTOR, 'span.pdp-price.pdp-price_type_normal').text
            product_data["price"] = price
        except:
            product_data["price"] = "N/A"

        try:
            actual_price = driver.find_element(By.CSS_SELECTOR, 'span.pdp-price.pdp-price_type_deleted').text
            product_data["actual_price"] = actual_price
        except:
            product_data["actual_price"] = "N/A"

        try:
            product_rating = driver.find_element(By.CLASS_NAME, 'pdp-review-summary')
            ratings_a_tag = product_rating.find_element(By.CSS_SELECTOR, 'a.pdp-link.pdp-link_size_s.pdp-link_theme_blue')
            ratings_text = ratings_a_tag.text
            product_data["ratings"] = ratings_text
        except:
            product_data["ratings"] = "N/A"

        try:
            div_element = driver.find_element(By.CLASS_NAME, 'sku-prop-content-header')
            span_element = div_element.find_element(By.TAG_NAME, 'span')
            span_text = span_element.text
            product_data["color"] = span_text
        except:
            product_data["color"] = "N/A"

    except Exception as e:
        print(f"Error extracting data from {link}: {e}")

    return product_data

# Main script
page_number = 1
max_pages = 30  # Limit pages for testing
all_product_links = []
base_url = "https://www.daraz.com.np/catalog/?_keyori=ss&from=search_history&q=laptop&spm=a2a0e.pdp_revamp.search.2.33501a61BsuXnk&page="

# CSV file setup
csv_file = "product_data.csv"
csv_columns = ["link", "product_title", "price", "actual_price", "ratings", "color"]

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()  # Write the headers

    # Loop through pages
    while page_number <= max_pages:
        print(f"Collecting links from page {page_number}")
        driver.get(base_url + str(page_number))
        
        # WebDriverWait for elements to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.RfADt a")))
        
        # Collect product links from the current page
        links = collect_product_links()

        # If no more links are found, break the loop
        if not links:
            print("No more product links found. Stopping.")
            break

        # Add the collected links to the list
        all_product_links.extend(links)

        # Go to the next page
        page_number += 1

    # Visit each collected link and extract product data
    for link in all_product_links:
        product_data = extract_product_data(link)
        writer.writerow(product_data)  # Write each product's data to the CSV file

# Close the browser
driver.quit()
