from page_object_pattern.pages.base_page import BasePage


class CheckoutPage(BasePage):

    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'

    def fill_customer_data(self, first_name, last_name, postal_code):
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)