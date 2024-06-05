from playwright.sync_api import Page

class LoginPage:
    # Variables - Would normally use AWS Security key provider[AWS Secrets-manager] or Azure[AZURE Key Valut] for the key managment to import credentials
    URL = 'https://qa-joeb.vermontsystems.com/wbwsc/webtrac_QATEST.wsc/login.html'
    username = '********' # Removed for security purposes
    password = '********' # Removed for security purposes
    
    # Locators + Constructor
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_field = page.locator('link:text("My Account Sign In / Register")')
        self.password_field = page.locator('label:text("Password *")')
        self.login_button = page.locator('button:text("Login")')
        self.logout_button = page.locator('link:text("Logout")')
        self.login_button_post_login = page.locator('link:text("Amanda VSTest #")')

    # Actions
    def load(self) -> None:
        self.page.goto(self.URL) # Will error without token by design

    def click_username_field(self):
        self.username_field.click()

    def fill_username_field(self, username):
        self.username_field.fill(username)

    def click_password_field(self):
        self.password_field.click()

    def fill_password_field(self, password):
        self.password_field.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def click_post_login_button(self):
        self.login_button_post_login.click()

    # Assertions
    def assert_login_button_authenticated(self):
        self.login_button_post_login.expect_visibility_state("visible")

    def assert_logout_button_is_visible(self):
        self.logout_button.expect_visibility_state("visible")