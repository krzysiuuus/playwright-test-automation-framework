import pytest
from playwright.sync_api import expect
from test_data.test_data import TEST_USERNAME, TEST_PASSWORD, TEST_PRODUCT_NAME

pytestmark = pytest.mark.ui


@pytest.mark.regression
def test_add_product_to_cart(
        page,
        login_page,
        inventory_page,
        cart_page,
        base_url
):
    login_page.open_login_page(base_url)
    login_page.login(TEST_USERNAME, TEST_PASSWORD)

    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    expect(page).to_have_url(f"{base_url}/cart.html")
    expect(cart_page.get_title()).to_have_text("Your Cart")
    expect(cart_page.get_product_names()).to_contain_text(TEST_PRODUCT_NAME)


@pytest.mark.regression
def test_add_two_products_to_cart(
        login_page,
        inventory_page,
        cart_page,
        base_url
):
    login_page.open_login_page(base_url)
    login_page.login(TEST_USERNAME, TEST_PASSWORD)

    inventory_page.add_product_to_cart("sauce-labs-backpack")
    inventory_page.add_product_to_cart("sauce-labs-bike-light")

    expect(inventory_page.get_cart_badge()).to_have_text("2")

    inventory_page.open_cart()

    expect(
        cart_page.get_product_by_name("Sauce Labs Backpack")
    ).to_be_visible()

    expect(
        cart_page.get_product_by_name("Sauce Labs Bike Light")
    ).to_be_visible()