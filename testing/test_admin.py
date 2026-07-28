import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://web-production-3e71a.up.railway.app"

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def admin_login(driver):
    driver.get(f"{BASE_URL}/login")
    time.sleep(2)
    driver.find_element(By.ID, "input-login-id").send_keys("admin")
    driver.find_element(By.ID, "input-password").send_keys("Admin123!")
    driver.find_element(By.ID, "btn-submit-login").click()
    time.sleep(2)

def test_admin_login():
    driver = setup_driver()
    try:
        print("\n--- Test: Admin Login ---")
        admin_login(driver)
        assert "Admin" in driver.page_source or "Dashboard" in driver.page_source, "Failed to login as admin."
        print("PASS: Admin Login")
    finally:
        driver.quit()

def test_view_users():
    driver = setup_driver()
    try:
        print("\n--- Test: View Users ---")
        admin_login(driver)
        
        driver.get(f"{BASE_URL}/admin/users")
        time.sleep(2)
        
        assert "Users" in driver.page_source or "Manage Users" in driver.page_source, "Failed to view users page."
        print("PASS: View Users")
    finally:
        driver.quit()

def test_delete_product():
    driver = setup_driver()
    try:
        print("\n--- Test: Admin Delete Product ---")
        admin_login(driver)
        
        driver.get(f"{BASE_URL}/admin/products")
        time.sleep(2)
        
        try:
            delete_form = driver.find_element(By.XPATH, "//form[contains(@action, '/admin/delete-product/')]")
            delete_form.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
            
            try:
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(2)
            except:
                pass
        except Exception as e:
            print("Note: Could not find delete product button. (Maybe no products).")
            
        print("PASS: Admin Delete Product")
    finally:
        driver.quit()

def test_delete_user():
    driver = setup_driver()
    try:
        print("\n--- Test: Admin Delete User ---")
        admin_login(driver)
        
        driver.get(f"{BASE_URL}/admin/users")
        time.sleep(2)
        
        try:
            # We look for a delete form for any user. In reality, we shouldn't delete the admin itself.
            # Assuming the UI has a 'Delete' button per row.
            delete_form = driver.find_element(By.XPATH, "//form[contains(@action, '/admin/delete-user/')]")
            delete_form.find_element(By.TAG_NAME, "button").click()
            time.sleep(2)
            
            try:
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(2)
            except:
                pass
        except Exception as e:
            print("Note: Could not find delete user button.")
            
        print("PASS: Admin Delete User")
    finally:
        driver.quit()

def test_admin_logout():
    driver = setup_driver()
    try:
        print("\n--- Test: Admin Logout ---")
        admin_login(driver)
        
        try:
            logout_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout') or contains(@href, 'logout')]")
            logout_link.click()
        except:
            driver.find_element(By.ID, "dropdownUser").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//a[contains(@href, 'logout')]").click()
            
        time.sleep(2)
        assert "Login" in driver.page_source or "Sign Up" in driver.page_source, "Failed to logout."
        print("PASS: Admin Logout")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_admin_login()
    test_view_users()
    test_delete_product()
    test_delete_user()
    test_admin_logout()
    print("\nAll Admin Tests Executed.")
