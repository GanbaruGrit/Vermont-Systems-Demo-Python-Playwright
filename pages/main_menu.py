from playwright.sync_api import Page

class MainMenuPage:
    def __init__(self, page: Page):
        self.page = page

    URL = 'https://qa-joeb.vermontsystems.com/wbwsc/webtrac_QATEST.wsc/splash.html?InterfaceParameter=WebTrac_NextGen/'

    def load(self) -> None:
        self.page.goto(self.URL)

    # Locators
    def __init__(self, page: Page) -> None:
        self.page = page
        self.my_account_button = page.locator('link:text("My Account Sign In / Register")')
        self.search_button = page.locator('link:text("Search")')
        self.make_donation_button = page.locator('link:text("Make A Donation")')
        self.reprint_receipt_button = page.locator('link:text("Reprint A Receipt")')

    # Actions
    def click_my_account_button(self) -> None:
        self.my_account_button.click()

    def click_search_button(self) -> None:
        self.search_button.click()

    def click_make_donation_button(self) -> None:
        self.make_donation_button.click()

    # Assertions
    def assert_title_is_visible(self):
        self.page.expect_title("WebTrac Next Gen (QATest) - Splash")

    def assert_search_button_is_visible(self):
        self.search_button.expect_visibility_state("visible")

    def assert_make_donation_button_is_visible(self):
        self.make_donation_button.expect_visibility_state("visible")