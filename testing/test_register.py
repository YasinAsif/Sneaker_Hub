import time
import random
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

def test_valid_registration():
    driver = setup_driver()
    try:
        print("\n--- Test: Valid Registration ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        # Generate a random username/email to avoid duplicate errors on repeated runs
        rand_id = random.randint(1000, 9999)
        username = f"testuser_{rand_id}"
        email = f"test_{rand_id}@sneakerhub.com"
        
        driver.find_element(By.ID, "input-first-name").send_keys("Test")
        driver.find_element(By.ID, "input-last-name").send_keys("User")
        driver.find_element(By.ID, "input-username").send_keys(username)
        driver.find_element(By.ID, "input-email").send_keys(email)
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        js_click(driver, By.ID, "btn-submit-register")
        time.sleep(3)
        
        # Verify redirect to login page
        assert "login" in driver.current_url or "Login" in driver.title, "Failed to redirect to login page."
        print("PASS: Valid Registration")
    finally:
        driver.quit()

def test_duplicate_email():
    driver = setup_driver()
    try:
        print("\n--- Test: Duplicate Email ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        # Using the buyer1@sneakerhub.com which exists in the seeded db
        driver.find_element(By.ID, "input-first-name").send_keys("Test")
        driver.find_element(By.ID, "input-last-name").send_keys("User")
        driver.find_element(By.ID, "input-username").send_keys("new_username_123")
        driver.find_element(By.ID, "input-email").send_keys("buyer1@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        js_click(driver, By.ID, "btn-submit-register")
        time.sleep(3)
        
        # Verify error
        page_source = driver.page_source
        assert "already registered" in page_source.lower() or "exists" in page_source.lower(), "Duplicate email error not displayed."
        print("PASS: Duplicate Email")
    finally:
        driver.quit()

def test_duplicate_username():
    driver = setup_driver()
    try:
        print("\n--- Test: Duplicate Username ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        driver.find_element(By.ID, "input-first-name").send_keys("Test")
        driver.find_element(By.ID, "input-last-name").send_keys("User")
        driver.find_element(By.ID, "input-username").send_keys("buyer1") # Seeded user
        driver.find_element(By.ID, "input-email").send_keys(f"random_{random.randint(100,999)}@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        js_click(driver, By.ID, "btn-submit-register")
        time.sleep(3)
        
        page_source = driver.page_source
        assert "already taken" in page_source.lower() or "exists" in page_source.lower(), "Duplicate username error not displayed."
        print("PASS: Duplicate Username")
    finally:
        driver.quit()

def test_weak_password():
    driver = setup_driver()
    try:
        print("\n--- Test: Weak Password ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        driver.find_element(By.ID, "input-first-name").send_keys("Test")
        driver.find_element(By.ID, "input-last-name").send_keys("User")
        driver.find_element(By.ID, "input-username").send_keys("weakpassuser")
        driver.find_element(By.ID, "input-email").send_keys("weakpass@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("123")
        driver.find_element(By.ID, "input-confirm-password").send_keys("123")
        js_click(driver, By.ID, "btn-submit-register")
        time.sleep(3)
        
        # Verify that we stayed on register page due to weak password or HTML5 validation
        assert "register" in driver.current_url or "Register" in driver.title, "Weak password was accepted."
        print("PASS: Weak Password")
    finally:
        driver.quit()

def test_invalid_email():
    driver = setup_driver()
    try:
        print("\n--- Test: Invalid Email ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        driver.find_element(By.ID, "input-first-name").send_keys("Test")
        driver.find_element(By.ID, "input-last-name").send_keys("User")
        driver.find_element(By.ID, "input-username").send_keys("invalidemailuser")
        driver.find_element(By.ID, "input-email").send_keys("not-an-email")
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        js_click(driver, By.ID, "btn-submit-register")
        time.sleep(3)
        
        assert "register" in driver.current_url or "Register" in driver.title, "Invalid email was accepted."
        print("PASS: Invalid Email")
    finally:
        driver.quit()

def test_empty_fields():
    driver = setup_driver()
    try:
        print("\n--- Test: Empty Fields ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        js_click(driver, By.ID, "btn-submit-register")
        time.sleep(2)
        
        assert "register" in driver.current_url or "Register" in driver.title, "Empty fields were accepted."
        print("PASS: Empty Fields")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_valid_registration()
    test_duplicate_email()
    test_duplicate_username()
    test_weak_password()
    test_invalid_email()
    test_empty_fields()
    print("\nAll Registration Tests Executed.")
