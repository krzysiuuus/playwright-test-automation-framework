import allure
from playwright.sync_api import expect


@allure.feature("Network Mocking")
@allure.title("Mock API response using Playwright page.route")
def test_mock_api_response(page):

    def mock_user_response(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"name": "Mocked User"}'
        )

    page.route("**/api/user", mock_user_response)

    page.goto("https://example.com")

    page.evaluate("""
        async () => {
            const response = await fetch('/api/user');
            const data = await response.json();

            const element = document.createElement('div');
            element.id = 'user-name';
            element.textContent = data.name;

            document.body.appendChild(element);
        }
    """)

    expect(page.locator("#user-name")).to_have_text("Mocked User")