from playwright.sync_api import expect

from test_data.test_data import TEST_USERNAME, TEST_PASSWORD


def test_successful_login(page, login_page, inventory_page, base_url):
    login_page.open_login_page(base_url)
    login_page.login(TEST_USERNAME, TEST_PASSWORD)

    expect(page).to_have_url(f"{base_url}/inventory.html")
    expect(inventory_page.get_title()).to_have_text("Products")
    expect(inventory_page.get_inventory_list()).to_be_visible()