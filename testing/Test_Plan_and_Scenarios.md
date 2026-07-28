# Test Plan & Scenarios

## 1. Introduction
This document outlines the test plan and scenarios for the **SneakerHub E-Commerce Platform**. The testing focuses on verifying the core functional modules using automated Selenium WebDriver scripts written in Python.

## 2. Scope
The testing scope covers the fundamental user flows of the application:
- User Authentication (Login / Logout)
- User Registration
- Search and Filtering
- Shopping Cart Operations
- Checkout Process
- Seller Dashboard Features
- Admin Dashboard Features

## 3. Environment
- **Target URL:** `https://yasif9155.pythonanywhere.com`
- **Testing Tool:** Selenium WebDriver (Python)
- **Browser:** Google Chrome
- **Driver Management:** `webdriver-manager`

## 4. Test Scenarios

### 4.1 Login Scenarios
- Verify successful login with valid credentials.
- Verify error handling for invalid password.
- Verify error handling for unregistered email.
- Verify form validation when fields are left empty.
- Verify password field is masked (type="password").
- Verify successful logout operation.

### 4.2 Registration Scenarios
- Verify successful registration of a new user.
- Verify system prevents duplicate email registration.
- Verify system prevents duplicate username registration.
- Verify validation for weak/short passwords.
- Verify validation for malformed email addresses.
- Verify form behavior when required fields are empty.

### 4.3 Search Scenarios
- Verify search function returns relevant results for existing brands (e.g., "Nike").
- Verify search handles non-existent queries properly.
- Verify search handles empty input.
- Verify search handles special characters safely.

### 4.4 Filter Scenarios
- Verify products can be filtered by Brand.
- Verify products can be filtered by Size.
- Verify products can be filtered by Color.
- Verify products can be filtered by Price Range.
- Verify filters can be cleared successfully.

### 4.5 Cart Scenarios
- Verify a product can be added to the cart.
- Verify a product can be removed from the cart.
- Verify item quantity can be increased.
- Verify item quantity can be decreased.
- Verify behavior when viewing an empty cart.

### 4.6 Checkout Scenarios
- Verify an order can be completed with valid details.
- Verify checkout fails if address is missing.
- Verify checkout fails if phone number is missing.
- Verify checkout fails with an invalid phone format.

### 4.7 Seller Dashboard Scenarios
- Verify a seller can add a new product.
- Verify a seller can edit an existing product's details.
- Verify a seller can delete a product.
- Verify product image upload functionality.

### 4.8 Admin Dashboard Scenarios
- Verify admin login functionality.
- Verify admin can view all registered users.
- Verify admin can delete a user.
- Verify admin can delete a product.
