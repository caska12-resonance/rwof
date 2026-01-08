from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto("http://localhost:8000")

        # Start the game
        page.locator('text="Astute Tutelage"').click()

        # Check for the rules button and click it
        rules_button = page.locator('button:has-text("?")')
        if not rules_button.is_visible():
            print("FAILURE: Rules button is not visible.")
            return

        rules_button.click()
        print("SUCCESS: Rules button clicked.")

        # Check if the modal is visible
        modal = page.locator('div:has-text("Come Giocare")').first
        if not modal.is_visible():
            print("FAILURE: Rules modal did not appear.")
            return

        print("SUCCESS: Rules modal is visible.")

        # Close the modal
        page.locator('button:has-text("CHIUDI")').click()

        # Check if the modal is hidden
        if modal.is_visible():
            print("FAILURE: Rules modal did not close.")
            return

        print("SUCCESS: Rules modal is hidden.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
