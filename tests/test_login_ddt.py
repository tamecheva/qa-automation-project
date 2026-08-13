import pytest
from playwright.sync_api import sync_playwright
import json

# Зареждане на данните от JSON файла
with open("login_data.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

# Генериране на параметри за pytest от JSON масива
@pytest.mark.parametrize("user_data", test_data)
def test_login(user_data):
    with sync_playwright() as p:
        # Важно: Уверете се, че headless=True за GitHub Actions
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Отиваме на страницата на SauceDemo
        page.goto("https://www.saucedemo.com/")
        
        # 2. ТУК СЛАГАМЕ ИЗЧАКВАНЕТО (преди да започнем да пишем в полетата)
        page.wait_for_selector("#user-name")
        
        # 3. Въвеждаме данните от JSON масива
        page.fill("#user-name", user_data["username"])
        page.fill("#password", user_data["password"])
        page.click("#login-button")

        # 4. Проверяваме очаквания резултат според JSON файла
        if user_data["should_succeed"] is True:
            # Успешен вход
            assert "/inventory.html" in page.url
        else:
            # Неуспешен вход (очакваме грешка)
            page.wait_for_selector("h3[data-test='error']")
            error_element = page.locator("h3[data-test='error']")
            assert error_element.is_visible()
            
        browser.close()
            
