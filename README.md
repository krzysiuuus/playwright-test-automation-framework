# Playwright Test Automation Framework

![Playwright Tests](https://github.com/krzysiuuus/playwright-test-automation-framework/actions/workflows/playwright-tests.yml/badge.svg)

Automated test framework created with Python, Playwright and Pytest.

The project contains both UI and API automated tests built around Page Object Model, native Playwright browser automation, Playwright API testing and reusable pytest fixtures.

The framework includes end-to-end UI scenarios, API validation, cross-browser execution, parallel execution, network mocking, Docker, Jenkins, GitHub Actions, Allure reporting and Playwright debugging artifacts.

## Technologies

- Python
- Playwright
- Pytest
- pytest-playwright
- Playwright APIRequestContext
- Page Object Model
- pytest-xdist
- pytest-rerunfailures
- Allure Reports
- Docker
- Jenkins
- GitHub Actions

## Features

- Page Object Model architecture
- Reusable page classes
- Thin BasePage implementation
- Native Playwright locators and actions
- UI and API automated tests
- End-to-end checkout scenario
- Playwright API testing
- Network interception and mocking with `page.route()`
- Chromium, Firefox and WebKit support
- Parallel test execution with pytest-xdist
- Playwright auto-waiting
- Trace collection on test failure
- Screenshots on test failure
- Video recording on test failure
- Allure reporting with business-level steps
- Optional retry support for flaky tests
- Dockerized test execution
- Jenkins CI pipeline
- Automatic Jenkins builds using SCM polling
- GitHub Actions CI
- Cross-browser execution in CI
- Test artifacts collected from CI runs

## Architecture

The framework separates test logic from page implementation and browser execution details.

Main concepts:

- Page Object Model for UI automation
- reusable page classes
- locators stored directly in Page Objects
- thin `BasePage` containing only shared page behavior
- pytest fixtures for setup and dependency injection
- separate UI and API test suites
- Playwright-native browser management
- Playwright-native API request context
- Allure integration
- Docker-based execution
- CI/CD using GitHub Actions and Jenkins

Unlike the Selenium framework, this project intentionally does not implement a custom Browser Factory or Selenium Grid. Browser creation, browser contexts, page lifecycle, auto-waiting and cross-browser execution are provided directly by Playwright and `pytest-playwright`.

### UI execution flow

```text
Test
  ↓
Page Object
  ↓
Playwright Page
  ↓
Browser Context
  ↓
Chromium / Firefox / WebKit
```

### API execution flow

```text
API Test
  ↓
Pytest Fixture
  ↓
Playwright APIRequestContext
  ↓
HTTP Request
  ↓
REST API
```

### Network mocking flow

```text
Browser request
  ↓
page.route()
  ↓
Route handler
  ↓
route.fulfill()
  ↓
Mocked API response
  ↓
UI validation
```

## Project Structure

```text
playwright-test-automation-framework/
├── .github/
│   └── workflows/
│       └── playwright-tests.yml
│
├── api_tests/
│   ├── __init__.py
│   └── test_users_api.py
│
├── page_objects/
│   ├── __init__.py
│   └── pages/
│       ├── __init__.py
│       ├── base_page.py
│       ├── login_page.py
│       ├── inventory_page.py
│       ├── cart_page.py
│       ├── checkout_page.py
│       ├── checkout_overview_page.py
│       └── checkout_complete_page.py
│
├── test_data/
│   ├── __init__.py
│   └── test_data.py
│
├── tests/
│   ├── test_cart.py
│   ├── test_checkout.py
│   ├── test_example.py
│   ├── test_login.py
│   └── test_network_mocking.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/krzysiuuus/playwright-test-automation-framework.git
cd playwright-test-automation-framework
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

## Running Tests

The project configuration is stored in `pytest.ini`.

The default base URL is:

```text
https://www.saucedemo.com
```

### Run all tests

```bash
pytest
```

This runs:

- UI tests in Chromium
- API tests
- Allure result generation
- Playwright failure artifacts according to `pytest.ini`

### Run UI tests

```bash
pytest tests
```

### Run UI tests with a visible browser

```bash
pytest tests --headed
```

### Run API tests

```bash
pytest api_tests -v
```

### Run selected test

Example:

```bash
pytest tests/test_login.py -v
```

## Cross-Browser Execution

Playwright supports three browser engines used by this framework:

- Chromium
- Firefox
- WebKit

Run UI tests in Chromium:

```bash
pytest tests --browser chromium
```

Run UI tests in Firefox:

```bash
pytest tests --browser firefox
```

Run UI tests in WebKit:

```bash
pytest tests --browser webkit
```

Run the UI suite across all supported browser engines:

```bash
pytest tests --browser chromium --browser firefox --browser webkit
```

Run all UI and API tests while executing the UI suite across all supported browser engines:

```bash
pytest --browser chromium --browser firefox --browser webkit
```

## Parallel Execution

Parallel execution is implemented with `pytest-xdist`.

Run tests using automatically selected workers:

```bash
pytest tests -n auto
```

Run cross-browser UI tests in parallel:

```bash
pytest tests -n auto \
    --browser chromium \
    --browser firefox \
    --browser webkit
```

The same approach is used in Jenkins CI.

## Playwright Browser Management

Browser lifecycle is handled by `pytest-playwright`.

The plugin provides reusable fixtures such as:

```text
playwright
browser
context
page
```

Tests can use the `page` fixture directly:

```python
def test_example(page):
    page.goto("https://example.com")
```

This avoids creating a custom browser factory and keeps browser management aligned with Playwright best practices.

## BasePage

The framework intentionally uses a minimal `BasePage`.

It contains only behavior that is genuinely shared between Page Objects, such as storing the Playwright `page` object and opening a URL.

Playwright actions remain native inside Page Objects, for example:

```python
self.page.locator(self.LOGIN_BUTTON).click()
self.page.locator(self.USERNAME_INPUT).fill(username)
```

This keeps Playwright-specific behavior visible and avoids unnecessary Selenium-style wrappers.

## Auto-Waiting

Playwright provides built-in auto-waiting for actions and web-first assertions.

The framework therefore does not introduce Selenium-style explicit wait wrappers for standard actions such as:

```python
locator.click()
locator.fill()
expect(locator).to_be_visible()
```

This reduces custom synchronization code and makes UI tests easier to maintain.

## API Testing

API automation uses Playwright's native `APIRequestContext`.

The request context is created as a pytest fixture and reused by API tests.

Implemented scenarios include:

- GET requests
- POST requests
- response status validation
- JSON response validation

Example endpoints are based on JSONPlaceholder.

Example:

```python
def test_get_user(api_request_context):
    response = api_request_context.get("/users/1")

    assert response.ok

    response_body = response.json()

    assert response_body["id"] == 1
```

The API suite does not depend on browser execution.

## Network Mocking

The project includes a network mocking example using Playwright's native request interception.

The test uses:

```python
page.route()
```

to intercept a browser request and:

```python
route.fulfill()
```

to return a controlled mock response without calling the real backend.

Example flow:

```text
GET /api/user
      ↓
Playwright intercepts request
      ↓
Mocked HTTP 200 response
      ↓
{"name": "Mocked User"}
      ↓
UI displays mocked value
      ↓
Playwright assertion
```

This demonstrates a Playwright-specific capability that can be used to test:

- backend errors
- empty responses
- specific test data
- unavailable services
- frontend behavior independent from a real backend

## Failure Diagnostics

The framework uses Playwright-native debugging artifacts.

Configured failure diagnostics include:

- trace
- screenshot
- video

The configuration is stored in `pytest.ini` using options such as:

```text
--tracing=retain-on-failure
--screenshot=only-on-failure
--video=retain-on-failure
```

Artifacts are written to:

```text
test-results/
```

### Trace Viewer

A saved trace can be opened with:

```bash
playwright show-trace path/to/trace.zip
```

Trace Viewer provides information such as:

- executed actions
- locators
- before/after page state
- DOM snapshots
- console output
- network activity
- source location

## Retry Support

The framework uses `pytest-rerunfailures`.

Retries are intentionally not enabled globally because global retries can hide real defects.

A known flaky test can be marked explicitly:

```python
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_unstable_scenario(page):
    ...
```

The custom marker is registered in `pytest.ini`.

This provides retry capability while keeping stable tests deterministic.

## Allure Reports

Allure integration is provided by `allure-pytest`.

Allure results are generated automatically through `pytest.ini`:

```text
--alluredir=allure-results
```

Run tests:

```bash
pytest
```

Open the report locally:

```bash
allure serve allure-results
```

Page Object business actions are decorated with `@allure.step`, making the report easier to read.

Example checkout flow in Allure:

```text
Open login page
Login as user
Add Sauce Labs Backpack to cart
Open shopping cart
Start checkout
Fill customer data
Continue checkout
Finish checkout
```

Allure is used for test reporting, while Playwright Trace Viewer is used for detailed technical debugging of failures.

## Docker

The project supports isolated test execution using Docker.

The Docker image is based on the official Playwright Python image:

```text
mcr.microsoft.com/playwright/python:v1.63.0-noble
```

The image provides the system environment required for Playwright browsers.

Project Python dependencies are installed from:

```text
requirements.txt
```

### Build Docker image

```bash
docker build -t playwright-test-framework .
```

### Run all tests

```bash
docker run --rm --ipc=host playwright-test-framework
```

### Run cross-browser UI tests

```bash
docker run --rm --ipc=host \
    playwright-test-framework \
    pytest tests \
    --browser chromium \
    --browser firefox \
    --browser webkit
```

The Docker environment provides reproducible Linux-based execution independent from the local Windows environment.

Unlike Selenium-based execution, Playwright does not require Selenium Grid or external browser nodes.

## Jenkins

The project is integrated with a shared Dockerized Jenkins environment.

Jenkins has:

- Docker CLI
- access to the host Docker Engine
- Allure integration

This allows the pipeline to build and run the Playwright test container directly.

The pipeline is defined as code in:

```text
Jenkinsfile
```

### Jenkins Pipeline

Pipeline flow:

```text
GitHub
   ↓
SCM Polling
   ↓
Jenkins
   ↓
Checkout
   ↓
Build Playwright Docker Image
   ↓
Run Tests in Docker
   ↓
Chromium / Firefox / WebKit
   ↓
Copy Test Artifacts
   ↓
Allure Report
```

The test container executes:

```bash
pytest -n auto \
    --browser chromium \
    --browser firefox \
    --browser webkit
```

API tests are also collected through the `testpaths` configuration in `pytest.ini`.

### Jenkins Test Artifacts

The Jenkins pipeline copies generated results from the Playwright test container before the container is removed.

Collected data includes:

```text
allure-results/
test-results/
```

`test-results/` can contain Playwright traces, screenshots and videos generated for failed tests.

Artifacts are archived by Jenkins for later analysis.

### Jenkins Allure Report

The Jenkins Allure plugin publishes results from:

```text
allure-results/
```

The report is generated in the `post` section of the pipeline so that test results remain available even if test execution fails.

### Automatic Jenkins Builds

Jenkins checks the Git repository using SCM polling:

```groovy
triggers {
    pollSCM('H/5 * * * *')
}
```

Jenkins periodically checks the repository and starts a new build only when a new commit is detected.

This avoids exposing a local Jenkins instance to the Internet through a webhook tunnel.

## GitHub Actions

GitHub Actions provides a second CI environment independent from Jenkins.

The workflow is defined in:

```text
.github/workflows/playwright-tests.yml
```

The workflow contains separate UI and API jobs.

### UI matrix

UI tests are executed independently for:

```text
Chromium
Firefox
WebKit
```

The GitHub Actions matrix creates a separate job for each browser engine.

UI tests are executed in parallel using `pytest-xdist`.

### API job

API tests run independently from browser jobs because browser installation is not required for API-only execution.

### Failure Artifacts

When a UI job fails, GitHub Actions uploads Playwright test artifacts from:

```text
test-results/
```

These artifacts can contain:

- trace files
- screenshots
- videos

### CI flow

```text
git push
   │
   ├── GitHub Actions
   │     ├── Chromium
   │     ├── Firefox
   │     ├── WebKit
   │     └── API tests
   │
   └── Jenkins SCM polling
         ↓
       Docker
         ↓
       Playwright tests
         ↓
       Allure Report
```

GitHub Actions and Jenkins operate independently.

## CI/CD Overview

The project currently supports four main execution approaches:

```text
1. LOCAL

pytest
├── UI tests
│   └── Chromium by default
└── API tests


2. LOCAL CROSS-BROWSER

pytest
└── UI tests
    ├── Chromium
    ├── Firefox
    └── WebKit


3. DOCKER

Docker
└── Playwright test container
    ├── UI tests
    │   ├── Chromium
    │   ├── Firefox
    │   └── WebKit
    └── API tests


4. CI

git push
├── GitHub Actions
│   ├── Chromium
│   ├── Firefox
│   ├── WebKit
│   └── API tests
│
└── Jenkins
    └── Docker
        └── Playwright tests
            ├── Chromium
            ├── Firefox
            ├── WebKit
            ├── API tests
            └── Allure Report
```

## Design Decisions

This framework intentionally uses Playwright-native functionality instead of reproducing Selenium abstractions.

Examples:

```text
Selenium                         Playwright
-------------------------------------------------------------
WebDriver                        Page
find_element()                   locator()
send_keys()                      fill()
WebDriverWait                    built-in auto-waiting
Browser Factory                  pytest-playwright fixtures
Chrome / Firefox / Edge          Chromium / Firefox / WebKit
custom failure screenshots       native trace / video / screenshot
Requests client                  Playwright APIRequestContext
external network tooling         page.route() / route.fulfill()
Selenium Grid                    Playwright browser runtime
```

The project keeps Page Object Model and CI concepts consistent with other automation frameworks while allowing Playwright-specific capabilities to remain visible.

## Future Improvements

Possible future extensions:

- additional API scenarios
- additional negative UI scenarios
- more advanced network interception examples
- environment-based configuration
- improved Allure metadata and test categorization
- test analytics and historical trend improvements

The project intentionally focuses on practical QA Automation concepts without unnecessary infrastructure complexity.

## Author

Created by [krzysiuuus](https://github.com/krzysiuuus)
