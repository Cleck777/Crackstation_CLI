from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Set up the Selenium WebDriver with headless option
options = webdriver.ChromeOptions()
options.add

options.headless = True
driver = webdriver.Chrome(options=options)

# Navigate to the web page
driver.get("https://192.168.56.101/login")

# Find the CSRF token element using its CSS selector
csrf_token_element = driver.find_element_by_css_selector("input[name='csrf_token']")

# Extract the CSRF token value
csrf_token = csrf_token_element.get_attribute("value")

# Print the CSRF token
print(csrf_token)

# Close the browser
driver.quit()
