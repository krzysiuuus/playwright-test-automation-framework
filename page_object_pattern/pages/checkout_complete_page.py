from page_object_pattern.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):

    TITLE = '[data-test="title"]'
    COMPLETE_HEADER = '[data-test="complete-header"]'

    def get_title(self):
        return self.get_locator(self.TITLE)

    def get_complete_header(self):
        return self.get_locator(self.COMPLETE_HEADER)