import allure
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@allure.feature("Navigation")
@allure.title("Open terms and conditions in a new tab")
@pytest.mark.regression
def test_terms_open_in_new_tab(page):

    page.context.route(
        "https://example.com/terms",
        lambda route: route.fulfill(
            status=200,
            content_type="text/html",
            body="<h1>Regulamin sklepu</h1>",
        ),
    )

    page.set_content(
        '<a href="https://example.com/terms" '
        'target="_blank">Regulamin</a>'
    )

    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Regulamin").click()

    terms_page = popup_info.value

    expect(terms_page).to_have_url(
        "https://example.com/terms"
    )

    expect(
        terms_page.get_by_role("heading", name="Regulamin sklepu")
    ).to_be_visible()