# test_login_ddt.py
import json
from playwright.sync_api import sync_playwright

# Функция за четене на външните тестови данни
def load_test_data():
    with open("login_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def run_data_driven_tests():
    test_cases = load_test_data()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        for index, data in enumerate(test_cases, start=1):
            print(f"\n--- Изпълнение на сценарий #{index} ---")
            print(f"Потребител: {data['username']} | Очакван успех: {data['should_succeed']}")
            
            # 1. Навигация до сайта
            page.goto("https://www.saucedemo.com/")
            
            # 2. Въвеждане на данни
            page.fill("#user-name", data["username"])
            page.fill("#password", data["password"])
            page.click("#login-button")
            
            if data["should_succeed"]:
                # Проверка при успешен вход (очакваме да зареди инвентара)
                assert "/inventory.html" in page.url, f"Сценарий #{index} падна: Очакваше се успешен вход!"
                print(f"Сценарий #{index}: Успешен вход (passed).")
                
                # Връщаме се назад или излизаме, за следващия тест
                page.goto("https://www.saucedemo.com/")
            else:
                # Проверка при неуспешен вход (очакваме съобщение за грешка)
                error_banner = page.locator("[data-test='error']")
                assert error_banner.is_visible(), f"Сценарий #{index} падна: Липсва съобщение за грешка!"
                print(f"Сценарий #{index}: Неуспешен вход, както беше очаквано (passed).")
                
        browser.close()
        print("\Всички Data-driven тестове приключиха успешно!")

if __name__ == "__main__":
    run_data_driven_tests()
