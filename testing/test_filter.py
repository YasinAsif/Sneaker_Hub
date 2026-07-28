import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

BASE_URL = "https://web-production-3e71a.up.railway.app"

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def test_brand_filter():
    driver = setup_driver()
    try:
        print("\n--- Test: Brand Filter ---")
        driver.get(f"{BASE_URL}/catalog")
        time.sleep(2)
        
        brand_select = Select(driver.find_element(By.ID, "filter-brand"))
        brand_select.select_by_value("nike")
        driver.find_element(By.ID, "btn-apply-filters").click()
        
        time.sleep(2)
        assert "Nike" in driver.page_source, "Brand filter failed."
        print("PASS: Brand Filter")
    finally:
        driver.quit()

def test_size_filter():
    driver = setup_driver()
    try:
        print("\n--- Test: Size Filter ---")
        driver.get(f"{BASE_URL}/catalog")
        time.sleep(2)
        
        size_select = Select(driver.find_element(By.ID, "filter-size"))
        size_select.select_by_value("10")
        driver.find_element(By.ID, "btn-apply-filters").click()
        
        time.sleep(2)
        assert "size=10" in driver.current_url, "Size filter not applied to URL."
        print("PASS: Size Filter")
    finally:
        driver.quit()

def test_color_filter():
    driver = setup_driver()
    try:
        print("\n--- Test: Color Filter ---")
        driver.get(f"{BASE_URL}/catalog")
        time.sleep(2)
        
        color_select = Select(driver.find_element(By.ID, "filter-color"))
        # We select by index 1 because the exact colors in DB might vary, but index 1 guarantees we pick a color
        color_select.select_by_index(1)
        driver.find_element(By.ID, "btn-apply-filters").click()
        
        time.sleep(2)
        assert "color=" in driver.current_url, "Color filter not applied to URL."
        print("PASS: Color Filter")
    finally:
        driver.quit()

def test_price_filter():
    driver = setup_driver()
    try:
        print("\n--- Test: Price Filter ---")
        driver.get(f"{BASE_URL}/catalog")
        time.sleep(2)
        
        driver.find_element(By.ID, "filter-min-price").send_keys("100")
        driver.find_element(By.ID, "filter-max-price").send_keys("200")
        driver.find_element(By.ID, "btn-apply-filters").click()
        time.sleep(2)
        
        assert "min_price=100" in driver.current_url, "Price filter not applied."
        print("PASS: Price Filter")
    finally:
        driver.quit()

def test_clear_filters():
    driver = setup_driver()
    try:
        print("\n--- Test: Clear Filters ---")
        driver.get(f"{BASE_URL}/catalog?brand=nike&min_price=100")
        time.sleep(2)
        
        driver.find_element(By.ID, "btn-clear-filters").click()
        time.sleep(2)
        assert "brand=nike" not in driver.current_url, "Filters were not cleared."
        print("PASS: Clear Filters")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_brand_filter()
    test_size_filter()
    test_color_filter()
    test_price_filter()
    test_clear_filters()
    print("\nAll Filter Tests Executed.")
