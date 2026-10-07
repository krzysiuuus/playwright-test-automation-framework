from page_objects.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):

    TITLE = '[data-test="title"]'
    COMPLETE_HEADER = '[data-test="complete-header"]'

    def get_title(self):
        return self.page.locator(self.TITLE)

    def get_complete_header(self):
        return self.page.locator(self.COMPLETE_HEADER)