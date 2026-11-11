import allure

from page_objects.pages.base_page import BasePage


class InventoryPage(BasePage):

    TITLE = '[data-test="title"]'
    INVENTORY_LIST = '[data-test="inventory-list"]'
    CART_LINK = '[data-test="shopping-cart-link"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'

    @allure.step("Add Sauce Labs Backpack to cart")
    def add_backpack_to_cart(self):
        self.add_product_to_cart("sauce-labs-backpack")

    @allure.step("Open shopping cart")
    def open_cart(self):
        self.page.locator(self.CART_LINK).click()

    def get_title(self):
        return self.page.locator(self.TITLE)

    def get_inventory_list(self):
        return self.page.locator(self.INVENTORY_LIST)

    #internal helper method, private method by convention
    def _get_add_to_cart_button(self, product_name):
        selector = f'[data-test="add-to-cart-{product_name}"]'
        return self.page.locator(selector)

    @allure.step("Add product to cart: {product_name}")
    def add_product_to_cart(self, product_name):
        self._get_add_to_cart_button(product_name).click()

    def get_cart_badge(self):
        return self.page.locator(self.CART_BADGE)