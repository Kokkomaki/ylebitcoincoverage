from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# Set up the Chrome driver
driver = webdriver.Chrome()

# Initialize a list to hold article data
article_data = []
article_counter = 1  # To track the index number of each article

# Loop through pages 1 to 45
for page_num in range(1, 46):  # Pages 1 through 45
    print(f"Processing page {page_num}...")

    # Construct the URL for the current page
    page_url = f"https://haku.yle.fi/?query=bitcoin&type=article&page={page_num}"
    driver.get(page_url)
    
    # Wait for the page to load
    time.sleep(5)

    # Accept cookies only once on the first page
    if page_num == 1:
        try:
            # Locate the "Hyväksy kaikki" button and click it
            accept_cookies_button = driver.find_element(By.XPATH, "//button[@name='accept-all-consents']")
            ActionChains(driver).move_to_element(accept_cookies_button).click().perform()
            print("Cookies accepted successfully.")
            time.sleep(2)  # Give it time to process the action
        except Exception as e:
            print(f"Cookie acceptance failed: {e}")

    # Find all article containers on the current page
    articles = driver.find_elements(By.CSS_SELECTOR, ".ArticleResults__SearchItemContainer-sc-858ijy-3")

    # Loop through each article container and collect URLs
    for index, article in enumerate(articles):
        try:
            # Find the link element within the article container
            link = article.find_element(By.TAG_NAME, "a")
            article_url = link.get_attribute("href")
            
            # Open the article link in the driver
            driver.get(article_url)
            time.sleep(3)

            # Scrape the article header (title)
            try:
                header = driver.find_element(By.XPATH, "//h1").text
            except Exception as e:
                header = f"Header not found: {e}"

            # Scrape the article content by targeting the specific classes found in the page source
            try:
                # Locate all paragraphs using the unique class patterns observed
                paragraphs = driver.find_elements(By.XPATH, "//section[contains(@class, 'yle__article__content')]//p[contains(@class, 'Paragraph-styles__Paragraph-sc-2000a27d-0') or contains(@class, 'Markdown-styles__Paragraph-sc-2429618e-0')]")
                
                # Join all the paragraph texts into a single content string
                content = ' '.join([para.text for para in paragraphs])
                if not content:  # In case the content is empty
                    content = "Content not found or empty"
            except Exception as e:
                content = f"Content not found: {e}"

            # Scrape the article publishing date
            try:
                date = driver.find_element(By.XPATH, "//time").get_attribute("datetime")
                if not date:
                    date = "Date not found"
            except Exception as e:
                date = f"Date not found: {e}"

            # Add data to the list with the specified structure
            article_data.append({
                'Index Number': article_counter,  # Index number of the article
                'Title': header,  # Article heading/title
                'Content': content,  # Article content
                'Date of Publishing': date,  # Date of publishing
                'URL': article_url  # Link to article
            })
            
            article_counter += 1  # Increment the article index counter

            # Return to the original search page
            driver.back()
            time.sleep(2)
            
        except Exception as e:
            print(f"Error processing article {index + 1} on page {page_num}: {e}")
            driver.back()  # Ensure we go back to the main page on error
            time.sleep(2)
            continue

# Save data to a CSV file
df = pd.DataFrame(article_data)
df.to_csv("scraped_articles.csv", index=False)
print("Scraping complete. Data saved to scraped_articles.csv.")

# Close the driver
driver.quit()

