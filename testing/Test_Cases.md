# Test Cases

| Test ID | Module | Test Case | Expected Result |
|---|---|---|---|
| TC-001 | Login | Login with valid credentials | Redirected to dashboard/home, profile/logout options visible |
| TC-002 | Login | Login with invalid password | "Invalid email or password" error displayed, stay on login page |
| TC-003 | Login | Login with unregistered username/email | "Invalid email or password" error displayed, stay on login page |
| TC-004 | Login | Submit empty login form | HTML5 validation triggers, or stay on login page |
| TC-005 | Login | Verify password field masking | Password input element has `type="password"` attribute |
| TC-006 | Login | Logout | Session ends, redirected to login/home page |
| TC-007 | Register | Valid Registration | Account created, redirected to login or dashboard |
| TC-008 | Register | Register with duplicate email | Error displayed indicating email is already in use |
| TC-009 | Register | Register with duplicate username | Error displayed indicating username is already taken |
| TC-010 | Register | Register with weak password | Password validation error displayed |
| TC-011 | Register | Register with invalid email format | HTML5 validation or application error displayed |
| TC-012 | Register | Submit empty registration form | HTML5 validation prevents submission |
| TC-013 | Search | Search existing brand (e.g., "Nike") | Catalog displays Nike products |
| TC-014 | Search | Search existing brand (e.g., "Adidas") | Catalog displays Adidas products |
| TC-015 | Search | Search non-existent string | "No products found" message displayed |
| TC-016 | Search | Submit empty search | Redirects to full catalog or stays on current page |
| TC-017 | Search | Search with special characters | Handled safely, shows "No products found" |
| TC-018 | Filter | Apply Brand Filter | URL updates, only products of selected brand shown |
| TC-019 | Filter | Apply Size Filter | URL updates, only products of selected size shown |
| TC-020 | Filter | Apply Color Filter | URL updates, only products of selected color shown |
| TC-021 | Filter | Apply Price Filter | URL updates, only products within price range shown |
| TC-022 | Filter | Clear Filters | Filters reset, URL clears query parameters |
| TC-023 | Cart | Add product to cart | Navigates to cart, item appears in list |
| TC-024 | Cart | Remove product from cart | Item removed, cart totals update |
| TC-025 | Cart | Increase product quantity | Quantity updates, price recalculates |
| TC-026 | Cart | Decrease product quantity | Quantity updates, price recalculates |
| TC-027 | Cart | View empty cart | "Empty cart" message displayed |
| TC-028 | Checkout | Complete checkout with valid details | Order confirmed, success message displayed |
| TC-029 | Checkout | Checkout with empty address | Form validation prevents submission |
| TC-030 | Checkout | Checkout with empty phone number | Form validation prevents submission |
| TC-031 | Checkout | Checkout with invalid phone format | Form validation prevents submission |
| TC-032 | Seller | Add new product | Product created, appears in dashboard/catalog |
| TC-033 | Seller | Edit product details | Changes saved and reflected in dashboard |
| TC-034 | Seller | Delete product | Product removed from database and dashboard |
| TC-035 | Seller | Upload product image | File accepted, image displays on product card |
| TC-036 | Admin | Admin Login | Redirected to admin dashboard successfully |
| TC-037 | Admin | View Users List | List of all registered users displayed |
| TC-038 | Admin | Delete User | User removed from system |
| TC-039 | Admin | Delete Product | Product removed from system |
