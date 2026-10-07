import pytest

from page_objects.pages.login_page import LoginPage
from page_objects.pages.inventory_page import InventoryPage
from page_objects.pages.cart_page import CartPage
from page_objects.pages.checkout_page import CheckoutPage
from page_objects.pages.checkout_overview_page import CheckoutOverviewPage
from page_objects.pages.checkout_complete_page import CheckoutCompletePage


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getini("base_url")


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def checkout_overview_page(page):
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page):
    return CheckoutCompletePage(page)


@pytest.fixture
def api_request_context(playwright):
    request_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )

    yield request_context

    request_context.dispose()