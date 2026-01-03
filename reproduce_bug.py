
from playwright.sync_api import sync_playwright, expect
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Listen for console events and print them
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

    try:
        page.goto("http://localhost:8000")

        # Click the "UMANI" faction button
        page.click("text=UMANI")

        # Wait for the player's hand to be visible and have cards
        p1_hand = page.locator("#p1Hand .card")

        # Check if there's at least one card in the hand.
        # This is the crucial check to see if the game has started correctly.
        expect(p1_hand.first).to_be_visible(timeout=5000)

        # Take a screenshot to verify the UI.
        page.screenshot(path="enhancements_applied.png")

        print("Test passed: Game started successfully, and player hand is rendered.")

    except Exception as e:
        print(f"Test failed: {e}")
        page.screenshot(path="error_enhancements.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
