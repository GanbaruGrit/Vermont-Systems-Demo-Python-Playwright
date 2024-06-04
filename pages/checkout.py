from playwright.sync_api import Page

class CheckoutPage:
    URL = 'https://qa-joeb.vermontsystems.com/wbwsc/webtrac_QATEST.wsc/checkout.html'
    test_cc_name = 'Amanda Lowry'
    test_cc_number = '4446 6612 3456 7892'
    test_cc_expiration_date = '06 / 26'
    test_cc_security_code = '999'
    test_cc_address = '123 Main St'
    test_cc_postal_code = '05446'

    def __init__(self, page: Page):
        self.page = page

    def load(self) -> None:
        self.page.goto(self.URL) # Will error without token by design

    # Locators
    def __init__(self, page: Page) -> None:
        self.page = page
        self.payment_method_button = page.locator('button:text("Using This Payment Method:")')
        self.visa_payment_method = page.locator('label:has-text("Select A Payment Method") >> text="Visa Payment"')
        self.cc_name = page.frame('name').locator('input')
        self.cc_number = page.frame('number').locator('input')
        self.cc_expiration_date = page.frame('expiration_date').locator('input')
        self.cc_security_code = page.frame('security_code').locator('input')
        self.cc_address = page.frame('address_line1').locator('input')
        self.cc_postal_code = page.frame('address_postal_code').locator('input')
        self.captcha_section = page.frame('[title="reCAPTCHA"]').locator('input[type="checkbox"]')
        self.continue_button = page.locator('button:text("Continue")')

    # Actions
    def click_payment_method_button(self):
        self.payment_method_button().click()

    def select_visa_payment_method(self):
        self.visa_payment_method().click()

    def fill_cc_name(self):
        self.cc_name().click()
        self.cc_name().fill(self.test_cc_name)

    def fill_cc_number(self):
        self.cc_number().click()
        self.cc_number().fill(self.test_cc_number)

    def fill_cc_expiration_date(self):
        self.cc_expiration_date().click()
        self.cc_expiration_date().fill(self.test_cc_expiration_date)

    def fill_cc_security_code(self):
        self.cc_security_code().click()
        self.cc_security_code().fill(self.test_cc_security_code)

    def fill_cc_address(self):
        self.cc_address().click()
        self.cc_address().fill(self.test_cc_address)

    def fill_cc_postal_code(self):
        self.cc_postal_code().click()
        self.cc_postal_code().fill(self.test_cc_postal_code)

    def click_captcha_section(self):
        self.captcha_section().click()

    def click_continue_button(self):
        self.continue_button().click()

    def fill_entire_cc_form(self):
        self.fill_cc_name()
        self.fill_cc_number()
        self.fill_cc_address()
        self.fill_cc_expiration_date()
        self.fill_cc_security_code()
        self.fill_cc_postal_code()

    # Assertions
    def assert_payment_method_button_is_visible(self):
        self.payment_method_button().expect_visibility_state("visible")

    def assert_cc_name_is_visible(self):
        self.cc_name().expect_visibility_state("visible")

    def assert_cc_number_is_visible(self):
        self.cc_number().expect_visibility_state("visible")

    def assert_cc_expiration_date_is_visible(self):
        self.cc_expiration_date().expect_visibility_state("visible")

    def assert_cc_security_code_is_visible(self):
        self.cc_security_code().expect_visibility_state("visible")

    def assert_cc_address_is_visible(self):
        self.cc_address().expect_visibility_state("visible")

    def assert_cc_postal_code_is_visible(self):
        self.cc_postal_code().expect_visibility_state("visible")

    def assert_captcha_section_is_visible(self):
        self.captcha_section().expect_visibility_state("visible")

    def assert_entire_cc_form(self):
        self.assert_cc_name_is_visible()
        self.assert_cc_number_is_visible()
        self.assert_cc_expiration_date_is_visible()
        self.assert_cc_security_code_is_visible()
        self.assert_cc_postal_code_is_visible()