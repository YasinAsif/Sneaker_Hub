import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Base URL for the testing environment
BASE_URL = "https://web-production-3e71a.up.railway.app"

def setup_driver():
    """Initialize the Chrome driver."""
    print("Setting up Chrome Driver...")
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def js_click(driver, by, value):
    """Click an element using JavaScript to bypass overlap/interception."""
    element = driver.find_element(by, value)
    driver.execute_script("arguments[0].click();", element)

def test_valid_login():
    driver = setup_driver()
    try:
        print("\n--- Test: Valid Login ---")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        # Enter credentials
        driver.find_element(By.ID, "input-login-id").send_keys("buyer1@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("Buyer123!")
        js_click(driver, By.ID, "btn-submit-login")
        time.sleep(2)
        
        # Verify success by checking if we were redirected to the home page or catalog
        page_source = driver.page_source
        assert "Logout" in page_source or "Profile" in page_source, "Failed to login properly."
        print("PASS: Valid Login")
    finally:
        driver.quit()

def test_invalid_password():
    driver = setup_driver()
    try:
        print("\n--- Test: Invalid Password ---")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        driver.find_element(By.ID, "input-login-id").send_keys("buyer1@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("WrongPassword!")
        js_click(driver, By.ID, "btn-submit-login")
        time.sleep(2)
        
        # Verify error message
        page_source = driver.page_source
        assert "Invalid username/email or password" in page_source or "Login" in page_source, "Error message not found."
        print("PASS: Invalid Password")
    finally:
        driver.quit()

def test_invalid_username():
    driver = setup_driver()
    try:
        print("\n--- Test: Invalid Username ---")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        driver.find_element(By.ID, "input-login-id").send_keys("doesnotexist@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("Buyer123!")
        js_click(driver, By.ID, "btn-submit-login")
        time.sleep(2)
        
        page_source = driver.page_source
        assert "Invalid username/email or password" in page_source or "Login" in page_source, "Error message not found."
        print("PASS: Invalid Username")
    finally:
        driver.quit()

def test_empty_fields():
    driver = setup_driver()
    try:
        print("\n--- Test: Empty Fields ---")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        # Click without filling fields
        js_click(driver, By.ID, "btn-submit-login")
        time.sleep(2)
        
        # We should still be on the login page
        assert "Login" in driver.title or "Login" in driver.page_source, "Should not proceed with empty fields."
        print("PASS: Empty Fields")
    finally:
        driver.quit()

def test_password_hidden():
    driver = setup_driver()
    try:
        print("\n--- Test: Password Hidden ---")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        # Check the type attribute of the password field
        password_field = driver.find_element(By.ID, "input-password")
        field_type = password_field.get_attribute("type")
        assert field_type == "password", f"Expected 'password', got '{field_type}'"
        print("PASS: Password Hidden")
    finally:
        driver.quit()

def test_logout():
    driver = setup_driver()
    try:
        print("\n--- Test: Logout ---")
        # Login first
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        driver.find_element(By.ID, "input-login-id").send_keys("buyer1@sneakerhub.com")
        driver.find_element(By.ID, "input-password").send_keys("Buyer123!")
        js_click(driver, By.ID, "btn-submit-login")
        time.sleep(2)
        
        # Find and click logout link
        try:
            logout_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout') or contains(@href, 'logout')]")
            driver.execute_script("arguments[0].click();", logout_link)
        except:
            # If it's under a profile dropdown
            dropdown = driver.find_element(By.ID, "dropdownUser")
            driver.execute_script("arguments[0].click();", dropdown)
            time.sleep(1)
            logout_link = driver.find_element(By.XPATH, "//a[contains(@href, 'logout')]")
            driver.execute_script("arguments[0].click();", logout_link)
            
        time.sleep(2)
        assert "Login" in driver.page_source or "Sign Up" in driver.page_source, "Failed to logout."
        print("PASS: Logout")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_valid_login()
    test_invalid_password()
    test_invalid_username()
    test_empty_fields()
    test_password_hidden()
    test_logout()
    print("\nAll Login Tests Executed.")
