from selenium import webdriver
from src import login, search

# Initialize driver
driver = webdriver.Firefox()

# Login
login.login(driver)

# Perform searches
search.run_searches(driver)