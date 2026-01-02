
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Serve the index.html file
            await page.goto(f"file:///app/index.html")

            # Wait for the faction selection screen to be visible
            await page.wait_for_selector("text=CONCLAVE ARCANA", timeout=10000)
            print("Faction selection screen loaded.")

            # Click the "CONCLAVE ARCANA" faction button
            await page.click("text=CONCLAVE ARCANA")
            print("Clicked 'CONCLAVE ARCANA' faction.")

            # Wait for the game board to be visible after faction selection
            await page.wait_for_selector(".board-area", timeout=10000)
            print("Game board loaded successfully.")

            # Take a screenshot
            screenshot_path = "arcanum_faction_test.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
            await page.screenshot(path="error_screenshot.png")
            print("Error screenshot saved.")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
