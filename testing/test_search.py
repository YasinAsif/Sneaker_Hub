import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://web-production-3e71a.up.railway.app"

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def test_search_nike():
    driver = setup_driver()
    try:
        print("\n--- Test: Search 'Nike' ---")
        driver.get(BASE_URL)
        time.sleep(2)
        
        search_input = driver.find_element(By.ID, "input-search")
        search_input.send_keys("Nike")
        driver.find_element(By.ID, "btn-search").click()
        time.sleep(2)
        
        page_source = driver.page_source
        assert "Nike" in page_source, "Nike products not found."
        print("PASS: Search 'Nike'")
    finally:
        driver.quit()

def test_search_adidas():
    driver = setup_driver()
    try:
        print("\n--- Test: Search 'Adidas' ---")
        driver.get(BASE_URL)
        time.sleep(2)
        
        search_input = driver.find_element(By.ID, "input-search")
        search_input.send_keys("Adidas")
        driver.find_element(By.ID, "btn-search").click()
        time.sleep(2)
        
        page_source = driver.page_source
        assert "Adidas" in page_source, "Adidas products not found."
        print("PASS: Search 'Adidas'")
    finally:
        driver.quit()

def test_search_nonexistent():
    driver = setup_driver()
    try:
        print("\n--- Test: Search Nonexistent Sneaker ---")
        driver.get(BASE_URL)
        time.sleep(2)
        
        search_input = driver.find_element(By.ID, "input-search")
        search_input.send_keys("XYZ123NonExistent")
        driver.find_element(By.ID, "btn-search").click()
        time.sleep(2)
        
        page_source = driver.page_source
        # Assuming the app shows a "No products found" message
        assert "No products found" in page_source or "0 results" in page_source.lower(), "Should show no results."
        print("PASS: Search Nonexistent Sneaker")
    finally:
        driver.quit()

def test_empty_search():
    driver = setup_driver()
    try:
        print("\n--- Test: Empty Search ---")
        driver.get(BASE_URL)
        time.sleep(2)
        
        driver.find_element(By.ID, "btn-search").click()
        time.sleep(2)
        
        # Depending on implementation, it might show all products or stay on home
        assert "SneakerHub" in driver.title, "Empty search failed."
        print("PASS: Empty Search")
    finally:
        driver.quit()

def test_search_special_characters():
    driver = setup_driver()
    try:
        print("\n--- Test: Search Special Characters ---")
        driver.get(BASE_URL)
        time.sleep(2)
        
        search_input = driver.find_element(By.ID, "input-search")
        search_input.send_keys("@#$%^&*()")
        driver.find_element(By.ID, "btn-search").click()
        time.sleep(2)
        
        page_source = driver.page_source
        assert "No products found" in page_source or "0 results" in page_source.lower(), "Should handle special characters safely."
        print("PASS: Search Special Characters")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_search_nike()
    test_search_adidas()
    test_search_nonexistent()
    test_empty_search()
    test_search_special_characters()
    print("\nAll Search Tests Executed.")
