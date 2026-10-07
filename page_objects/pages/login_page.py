import allure

from page_objects.pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'

    @allure.step("Open login page")
    def open_login_page(self, base_url):
        self.open(base_url)

    @allure.step("Login as user: {username}")
    def login(self, username, password):
        self.page.locator(self.USERNAME_INPUT).fill(username)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()