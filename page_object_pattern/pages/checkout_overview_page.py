from page_object_pattern.pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):

    TITLE = '[data-test="title"]'
    FINISH_BUTTON = '[data-test="finish"]'

    def get_title(self):
        return self.page.locator(self.TITLE)

    def finish_checkout(self):
        self.page.locator(self.FINISH_BUTTON).click()