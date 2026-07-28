import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://web-production-3e71a.up.railway.app"

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

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
        
        driver.find_element(By.ID, "input-username").send_keys(username)
        driver.find_element(By.ID, "input-email").send_keys(email)
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "btn-submit-register").click()
        time.sleep(3)
        
        # Verify redirect to login or dashboard
        assert "Login" in driver.title or "Login" in driver.page_source or "Home" in driver.page_source, "Failed to register successfully."
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
        driver.find_element(By.ID, "input-username").send_keys("new_username_123")
        driver.find_element(By.ID, "input-email").send_keys("buyer1@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "btn-submit-register").click()
        time.sleep(2)
        
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
        
        driver.find_element(By.ID, "input-username").send_keys("buyer1") # Seeded user
        driver.find_element(By.ID, "input-email").send_keys(f"random_{random.randint(100,999)}@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "btn-submit-register").click()
        time.sleep(2)
        
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
        
        driver.find_element(By.ID, "input-username").send_keys("weakpassuser")
        driver.find_element(By.ID, "input-email").send_keys("weakpass@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("123")
        driver.find_element(By.ID, "input-confirm-password").send_keys("123")
        driver.find_element(By.ID, "btn-submit-register").click()
        time.sleep(2)
        
        assert "Register" in driver.title or "Register" in driver.page_source, "Weak password was accepted."
        print("PASS: Weak Password")
    finally:
        driver.quit()

def test_invalid_email():
    driver = setup_driver()
    try:
        print("\n--- Test: Invalid Email ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        driver.find_element(By.ID, "input-username").send_keys("invalidemailuser")
        driver.find_element(By.ID, "input-email").send_keys("not-an-email")
        driver.find_element(By.ID, "input-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "input-confirm-password").send_keys("SecurePass123!")
        driver.find_element(By.ID, "btn-submit-register").click()
        time.sleep(2)
        
        assert "Register" in driver.title or "Register" in driver.page_source, "Invalid email was accepted."
        print("PASS: Invalid Email")
    finally:
        driver.quit()

def test_empty_fields():
    driver = setup_driver()
    try:
        print("\n--- Test: Empty Fields ---")
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        
        driver.find_element(By.ID, "btn-submit-register").click()
        time.sleep(2)
        
        assert "Register" in driver.title or "Register" in driver.page_source, "Empty fields were accepted."
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
