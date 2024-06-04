import pytest
from playwright.sync_api import Page
from pages.main_menu import MainMenuPage
from pages.login import LoginPage
from pages.donation import DonationPage
from pages.checkout import CheckoutPage

@pytest.fixture(scope="session")
def page_context(context):
    # Save storage state into the file. Speeds up authentication and is reusable.
    storage = context.storage_state(path="state.json")

    # Create a new context with the saved storage state. Create a snapshot of the session to re-use for testing.
    context = context.new_context(storage_state=storage)
    yield context

def test_setup(browser):
    browser.selectors.set_test_id_attribute("data-title") # matches Vermont Systems conventions

def test_add_donation_to_cart(page: Page):
    page.set_timeout(120000) # Intentionally high to compensate for receipt back-end and captcha delays present in WebTrac staging build
    
    # Page Object Model constructors
    main_menu_page = MainMenuPage(page)
    login_page = LoginPage(page)
    donation_page = DonationPage(page)
    checkout_page = CheckoutPage(page)

    # Login
    main_menu_page.goto(main_menu_page.URL)

    main_menu_page.assert_title_is_visible()
    main_menu_page.click_my_account_button()

    login_page.click_username_field()
    login_page.fill_username_field(login_page.username)

    login_page.click_password_field()
    login_page.fill_password_field(login_page.password)

    login_page.click_login_button()

    # Handle Potential Active Session
    if page.locator('heading:has-text("Login Warning - Active")').is_visible():
        page.locator('button:has-text("Continue with Login")').click()

    login_page.assert_login_button_authenticated()
    login_page.click_post_login_button()
    login_page.assert_logout_button_is_visible()

    print("Login Test - Passed")

    # Navigate and add donation to cart
    main_menu_page.assert_search_button_is_visible()
    main_menu_page.click_search_button()

    main_menu_page.assert_make_donation_button_is_visible()
    main_menu_page.click_make_donation_button()
    
    donation_page.assert_donate_radio_button_is_visible()
    donation_page.check_donate_radio_button()
    donation_page.assert_donate_radio_button_is_checked()

    donation_page.click_add_to_cart_button()
    donation_page.assert_donation_heading_is_visible()
    
    # Donation details
    donation_page.check_donation_add_radio_button()
    donation_page.assert_donation_add_radio_button_is_checked()

    donation_page.fill_donation_fee_field()
    donation_page.assert_donation_fee_field_has_value()

    donation_page.assert_continue_button_is_visible()
    donation_page.click_continue_button()

    donation_page.assert_donation_remove_button_is_visible()
    donation_page.assert_donation_description_is_visible()
    donation_page.assert_donation_name_is_visible()
    donation_page.assert_donation_total_fees_is_visible()
    donation_page.assert_checkout_button_is_visible()

    donation_page.click_proceed_checkout_button()

    # Checkout
    checkout_page.assert_payment_method_button_is_visible()
    checkout_page.click_payment_method_button()
    checkout_page.select_visa_payment_method()

    checkout_page.assert_cc_name_is_visible()
    checkout_page.fill_cc_name()

    checkout_page.assert_cc_number_is_visible()
    checkout_page.fill_cc_number()

    checkout_page.assert_cc_expiration_date_is_visible()
    checkout_page.fill_cc_expiration_date()

    checkout_page.assert_cc_security_code_is_visible()
    checkout_page.fill_cc_security_code()

    checkout_page.assert_cc_address_is_visible()
    checkout_page.fill_cc_address()

    checkout_page.assert_cc_postal_code_is_visible()
    checkout_page.fill_cc_postal_code()

    checkout_page.assert_captcha_section_is_visible()
    checkout_page.click_captcha_section()

    page.wait_for_timeout(8000) # Waiting for captcha to finish

    checkout_page.click_continue_button()

    # Confirmation Page
    donation_confirmation_number = page.locator('h3').inner_text()
    login_page.login_button_post_login().click()
    main_menu_page.reprint_receipt_button().click()
    
    page.wait_for_timeout(100000) # Waiting for receipt page to populate
    page.reload()

    receipt_locator = page.locator('td.label-cell[data-title="Number"]').first()
    receipt_confirmation_number = receipt_locator.inner_text()

    assert donation_confirmation_number == receipt_confirmation_number

    print("Do receipts match?", donation_confirmation_number, receipt_confirmation_number)
    
    # Handle PDF Pop-up & Download
    with page.expect_popup() as popup_info:
        with page.expect_download() as download_info:
            page.locator('link:has-text("Reprint Receipt")').first().click()
            page.wait_for_timeout(10000) # Waiting for download to finish
    popup = popup_info.value
    download = download_info.value
    
    print("file downloaded to", download.path())
    print("If pop-up, URL and Title:", popup.url, popup.title)

    login_page.login_button_post_login().click()
    login_page.logout_button().click()

@pytest.mark.parametrize("test_info", ["Test 1", "Test 2", "Test 3"]) # Example of parameterized test
def test_after_each(page, test_info):
    print(f"Finished {test_info} with status {page.title()}")

@pytest.fixture(scope="session")
def teardown(page):
    print('Clear carts, caches, and reset database')
    # Empty cart for clean test
    page.locator('link:has-text("Checkout Cart")').click()
    page.locator('link:has-text("Empty Cart")').click()
