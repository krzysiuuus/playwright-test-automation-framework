import os

import pytest
from dotenv import load_dotenv

from page_objects.pages.login_page import LoginPage
from page_objects.pages.inventory_page import InventoryPage
from page_objects.pages.cart_page import CartPage
from page_objects.pages.checkout_page import CheckoutPage
from page_objects.pages.checkout_overview_page import CheckoutOverviewPage
from page_objects.pages.checkout_complete_page import CheckoutCompletePage

load_dotenv()

@pytest.fixture(scope="session")
def reqres_base_url():
    return os.getenv("REQRES_BASE_URL")


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getini("base_url")


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL")


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
def api_request_context(playwright, api_base_url):
    request_context = playwright.request.new_context(
        base_url=api_base_url
    )

    yield request_context

    request_context.dispose()


@pytest.fixture(scope="session")
def reqres_api_key():
    return os.getenv("REQRES_API_KEY")


@pytest.fixture
def reqres_request_context(playwright, reqres_base_url, reqres_api_key):
    request_context = playwright.request.new_context(
        base_url=reqres_base_url,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": reqres_api_key,
            "X-Reqres-Env": "dev"
        }
    )

    yield request_context

    request_context.dispose()