from sys import last_value
from playwright.sync_api import Page

class DonationPage:
    URL = 'https://qa-joeb.vermontsystems.com/wbwsc/webtrac_QATEST.wsc/donation.html'
    test_value = 100
    
    def __init__(self, page: Page):
        self.page = page

    def load(self) -> None:
        self.page.goto(self.URL) # Will error without token by design

    # Locators
    def __init__(self, page: Page) -> None:
        self.page = page
        self.donate_radio_button = page.locator('label:text("Check to purchase Donation (")')
        self.search_button = page.locator('link:text("Search")')
        self.make_donation_button = page.locator('link:text("Make A Donation")')
        self.add_to_cart_button = page.locator('button:text("Add To Cart")')
        self.continue_button = page.locator('button:text("Continue")')
        self.proceed_checkout_button = page.locator('link:text("Proceed To Checkout")')
        self.donation_heading = page.locator('heading:text("Donation (enter $ Amt) (")').first()
        self.donation_add_radio_button = page.locator('svg.checkbox__check.svg-icon.svg-fill')
        self.donation_fee_field = self.page.locator('input:textbox').first()
        self.donation_quantity = page.locator('input.fillin.fieldid--9.disabled.decimal.text-left')
        self.donation_remove_button = page.locator('link:text("Remove")').first()
        self.donation_description = page.locator('cell:text("Donation (enter $ Amt) (")').first()
        self.donation_name = page.locator('cell:text("Amanda")').first()
        self.donation_total_fees = page.locator('cell:text("$ 100.00")').first()

    # Actions
    def check_donate_radio_button(self):
        self.donate_radio_button.check()

    def click_add_to_cart_button(self):
        self.add_to_cart_button.click()

    def click_continue_button(self):
        self.continue_button.click()

    def click_proceed_checkout_button(self):
        self.proceed_checkout_button.click()

    def check_donation_add_radio_button(self):
        self.donation_add_radio_button.check()

    def fill_donation_fee_field(self):
        self.donation_fee_field.fill(self.test_value)

    # Assertions
    def assert_continue_button_is_visible(self):
        self.continue_button.expect_visibility_state("visible")

    def assert_donate_radio_button_is_visible(self):
        self.donate_radio_button.expect_visibility_state("visible")

    def assert_donate_radio_button_is_checked(self):
        self.donate_radio_button.expect_state("checked")

    def assert_checkout_button_is_visible(self):
        self.proceed_checkout_button.expect_visibility_state("visible")

    def assert_donation_heading_is_visible(self):
        self.donation_heading.expect_visibility_state("visible")

    def assert_donation_add_radio_button_is_checked(self):
        self.donation_add_radio_button.expect_state("checked")

    def assert_donation_fee_field_has_value(self):
        self.donation_fee_field.expect_value(self.test_value)

    def assert_donation_remove_button_is_visible(self):
        self.donation_remove_button.expect_visibility_state("visible")

    def assert_donation_description_is_visible(self):
        self.donation_description.expect_visibility_state("visible")

    def assert_donation_name_is_visible(self):
        self.donation_name.expect_visibility_state("visible")

    def assert_donation_total_fees_is_visible(self):
        self.donation_total_fees.expect_visibility_state("visible")