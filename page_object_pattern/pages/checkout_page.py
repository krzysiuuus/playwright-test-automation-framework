from page_object_pattern.pages.base_page import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'

    def fill_customer_data(self, first_name, last_name, postal_code):
        self.page.locator(self.FIRST_NAME_INPUT).fill(first_name)
        self.page.locator(self.LAST_NAME_INPUT).fill(last_name)
        self.page.locator(self.POSTAL_CODE_INPUT).fill(postal_code)

    def continue_checkout(self):
        self.page.locator(self.CONTINUE_BUTTON).click()