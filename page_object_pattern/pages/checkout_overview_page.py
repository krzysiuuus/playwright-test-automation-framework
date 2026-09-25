from page_object_pattern.pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):

    TITLE = '[data-test="title"]'
    FINISH_BUTTON = '[data-test="finish"]'

    def get_title(self):
        return self.get_locator(self.TITLE)

    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)