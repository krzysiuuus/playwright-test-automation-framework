import allure

from page_objects.pages.base_page import BasePage


class CartPage(BasePage):

    TITLE = '[data-test="title"]'
    CART_ITEMS = '[data-test="inventory-item"]'
    PRODUCT_NAMES = '[data-test="inventory-item-name"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'

    def get_title(self):
        return self.page.locator(self.TITLE)

    def get_cart_items(self):
        return self.page.locator(self.CART_ITEMS)

    def get_product_names(self):
        return self.page.locator(self.PRODUCT_NAMES)

    def get_product_by_name(self, product_name):
        return self.page.locator(self.PRODUCT_NAMES).filter(
            has_text=product_name
        )

    @allure.step("Start checkout")
    def start_checkout(self):
        self.page.locator(self.CHECKOUT_BUTTON).click()