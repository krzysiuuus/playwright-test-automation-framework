from playwright.sync_api import expect

from test_data.test_data import (
    TEST_USERNAME,
    TEST_PASSWORD,
    TEST_PRODUCT_NAME,
    TEST_FIRST_NAME,
    TEST_LAST_NAME,
    TEST_POSTAL_CODE,
)


def test_complete_checkout(
        page,
        login_page,
        inventory_page,
        cart_page,
        checkout_page,
        checkout_overview_page,
        checkout_complete_page,
        base_url
):
    login_page.open_login_page(base_url)
    login_page.login(TEST_USERNAME, TEST_PASSWORD)

    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    expect(cart_page.get_title()).to_have_text("Your Cart")
    expect(
        cart_page.get_product_by_name(TEST_PRODUCT_NAME)
    ).to_be_visible()

    cart_page.start_checkout()

    checkout_page.fill_customer_data(
        TEST_FIRST_NAME,
        TEST_LAST_NAME,
        TEST_POSTAL_CODE
    )
    checkout_page.continue_checkout()

    expect(checkout_overview_page.get_title()).to_have_text(
        "Checkout: Overview"
    )

    checkout_overview_page.finish_checkout()

    expect(page).to_have_url(f"{base_url}/checkout-complete.html")
    expect(checkout_complete_page.get_title()).to_have_text(
        "Checkout: Complete!"
    )
    expect(checkout_complete_page.get_complete_header()).to_have_text(
        "Thank you for your order!"
    )