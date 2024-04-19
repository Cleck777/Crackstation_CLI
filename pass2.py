from seleniumwire import webdriver

##  Get the URL
driver = webdriver.Chrome()
driver.get("https://192.168.56.101/login")

##  Print request headers
for request in driver.requests:
  print(request.url) # <--------------- Request url
  print(request.headers) # <----------- Request headers
  print(request.response.headers) # <-- Response headers
