import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://web-production-3e71a.up.railway.app"

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def js_click(driver, by, value):
    """Click an element using JavaScript to bypass overlap/interception."""
    element = driver.find_element(by, value)
    driver.execute_script("arguments[0].click();", element)

def js_click_elem(driver, element):
    """Click a WebElement using JavaScript."""
    driver.execute_script("arguments[0].click();", element)

def quick_login(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "input-login-id").send_keys("buyer1@sneakerhub.com")
    driver.find_element(By.ID, "input-password").send_keys("Buyer123!")
    js_click(driver, By.ID, "btn-submit-login")
    time.sleep(2)

def navigate_to_in_stock_product(driver):
    """Finds the first in-stock product from the catalog page and navigates to it."""
    driver.get(f"{BASE_URL}/catalog")
    time.sleep(2)
    product_cards = driver.find_elements(By.CSS_SELECTOR, ".product-card")
    for idx in range(len(product_cards)):
        cards = driver.find_elements(By.CSS_SELECTOR, ".product-card")
        if idx >= len(cards):
            break
        card = cards[idx]
        link = card.find_element(By.CSS_SELECTOR, ".card-body a")
        product_url = link.get_attribute("href")
        driver.get(product_url)
        time.sleep(2)
        
        # Check if btn-add-to-cart is on the page
        buttons = driver.find_elements(By.ID, "btn-add-to-cart")
        if len(buttons) > 0:
            return
        
        driver.get(f"{BASE_URL}/catalog")
        time.sleep(2)
    raise Exception("No in-stock products found in the catalog!")

def add_product_to_cart(driver):
    navigate_to_in_stock_product(driver)
    js_click(driver, By.ID, "btn-add-to-cart")
    time.sleep(2)

def test_complete_checkout():
    driver = setup_driver()
    try:
        print("\n--- Test: Complete Checkout ---")
        quick_login(driver)
        add_product_to_cart(driver)
        
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(2)
        
        address_field = driver.find_element(By.ID, "input-address")
        address_field.clear()
        address_field.send_keys("123 Test Street, Testing City")
        
        phone_field = driver.find_element(By.ID, "input-phone")
        phone_field.clear()
        phone_field.send_keys("5551234567")
        
        js_click(driver, By.ID, "btn-place-order")
        time.sleep(3)
        
        assert "Order" in driver.page_source or "Success" in driver.page_source or "Orders" in driver.title, "Failed to complete checkout."
        print("PASS: Complete Checkout")
    finally:
        driver.quit()

def test_empty_address():
    driver = setup_driver()
    try:
        print("\n--- Test: Empty Address ---")
        quick_login(driver)
        add_product_to_cart(driver)
        
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(2)
        
        address_field = driver.find_element(By.ID, "input-address")
        address_field.clear() # Leave address empty
        
        phone_field = driver.find_element(By.ID, "input-phone")
        phone_field.clear()
        phone_field.send_keys("5551234567")
        
        js_click(driver, By.ID, "btn-place-order")
        time.sleep(2)
        
        assert "Checkout" in driver.title or "Checkout" in driver.page_source, "Empty address allowed checkout to proceed."
        print("PASS: Empty Address")
    finally:
        driver.quit()

def test_empty_phone_number():
    driver = setup_driver()
    try:
        print("\n--- Test: Empty Phone Number ---")
        quick_login(driver)
        add_product_to_cart(driver)
        
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(2)
        
        address_field = driver.find_element(By.ID, "input-address")
        address_field.clear()
        address_field.send_keys("123 Test Street")
        
        phone_field = driver.find_element(By.ID, "input-phone")
        phone_field.clear() # Leave phone empty
        
        js_click(driver, By.ID, "btn-place-order")
        time.sleep(2)
        
        assert "Checkout" in driver.title or "Checkout" in driver.page_source, "Empty phone allowed checkout to proceed."
        print("PASS: Empty Phone Number")
    finally:
        driver.quit()

def test_invalid_phone_number():
    driver = setup_driver()
    try:
        print("\n--- Test: Invalid Phone Number ---")
        quick_login(driver)
        add_product_to_cart(driver)
        
        driver.get(f"{BASE_URL}/checkout")
        time.sleep(2)
        
        address_field = driver.find_element(By.ID, "input-address")
        address_field.clear()
        address_field.send_keys("123 Test Street")
        
        phone_field = driver.find_element(By.ID, "input-phone")
        phone_field.clear()
        phone_field.send_keys("abc")
        
        js_click(driver, By.ID, "btn-place-order")
        time.sleep(2)
        
        assert "Checkout" in driver.title or "Checkout" in driver.page_source, "Invalid phone allowed checkout to proceed."
        print("PASS: Invalid Phone Number")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_complete_checkout()
    test_empty_address()
    test_empty_phone_number()
    test_invalid_phone_number()
    print("\nAll Checkout Tests Executed.")
