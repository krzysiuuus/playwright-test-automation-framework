from page_object_pattern.pages.base_page import BasePage


class InventoryPage(BasePage):

    TITLE = '[data-test="title"]'
    INVENTORY_LIST = '[data-test="inventory-list"]'
    ADD_BACKPACK_BUTTON = '[data-test="add-to-cart-sauce-labs-backpack"]'
    CART_LINK = '[data-test="shopping-cart-link"]'

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BUTTON)

    def open_cart(self):
        self.click(self.CART_LINK)

    def get_title(self):
        return self.get_locator(self.TITLE)

    def get_inventory_list(self):
        return self.get_locator(self.INVENTORY_LIST)