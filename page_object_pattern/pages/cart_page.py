from page_object_pattern.pages.base_page import BasePage


class CartPage(BasePage):

    TITLE = '[data-test="title"]'
    CART_ITEMS = '[data-test="inventory-item"]'
    PRODUCT_NAMES = '[data-test="inventory-item-name"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'

    def get_title(self):
        return self.get_locator(self.TITLE)

    def get_cart_items(self):
        return self.get_locator(self.CART_ITEMS)

    def get_product_names(self):
        return self.get_locator(self.PRODUCT_NAMES)

    def get_product_by_name(self, product_name):
        return self.page.locator(self.PRODUCT_NAMES).filter(
            has_text=product_name
        )

    def start_checkout(self):
        self.click(self.CHECKOUT_BUTTON)