import asyncio
from playwright.async_api import async_playwright, expect
import json
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}"))

        await page.goto(f"file://{os.path.abspath('index.html')}")

        print("Game state override injected.")

        p1_field_override = [
            {"name": "Custode del Velo", "strength": 2, "type": "Creatura", "rarity": 'epic', "effect": 'SACRIFICE_TO_PROTECT_MIRAGE', "desc": "Se un tuo Miraggio sta per essere distrutto, puoi scegliere di distruggere questa carta invece del Miraggio.", "faction": "arcanum", "uid": "custode-1", "currentStrength": 2, "tempStrength": 0},
            {"name": "Lupo di Vapore", "strength": 3, "type": "Creatura", "rarity": 'common', "effect": 'MIRAGE', "desc": "Miraggio.", "faction": "arcanum", "uid": "mirage-1", "currentStrength": 3, "tempStrength": 0}
        ]

        p2_hand_override = [
            {"name": "Colosso Prova", "strength": 3, "type": "Creatura", "rarity": 'common', "effect": 'NONE', "desc": "-", "faction": "beast", "uid": "ai-card-1", "currentStrength": 3, "tempStrength": 0},
            {"name": "Scarta1", "strength": 2, "type": "Creatura", "rarity": 'common', "effect": 'NONE', "desc": "-", "faction": "beast", "uid": "ai-card-2", "currentStrength": 2, "tempStrength": 0},
            {"name": "Scarta2", "strength": 1, "type": "Creatura", "rarity": 'common', "effect": 'NONE', "desc": "-", "faction": "beast", "uid": "ai-card-3", "currentStrength": 1, "tempStrength": 0}
        ]

        await page.evaluate(f"window.p1FieldOverride = {json.dumps(p1_field_override)}")
        await page.evaluate(f"window.p2HandOverride = {json.dumps(p2_hand_override)}")
        await page.evaluate("window.p1GraveOverride = []")
        await page.evaluate("window.p2FieldOverride = []")
        await page.evaluate("window.p2GraveOverride = []")
        await page.evaluate("window.startingPlayerOverride = 2")

        # Use the new, more reliable test hook to start the game
        await page.evaluate("window.startGameWithFaction = 'arcanum'")
        # The useEffect in the React app will now pick this up and start the game.
        # We might need a small delay or a check to ensure the game has started.
        await page.wait_for_function("() => window.gameState !== 'MENU'")


        print("Game started.")

        print("Waiting for choice modal...")
        try:
            await expect(page.locator("h2:has-text(\"Scegli una carta da distruggere per l'effetto avversario\")")).to_be_visible(timeout=10000)
            print("Choice modal found!")

            custode_locator = page.locator("div[data-testid='card-Custode del Velo']")
            mirage_locator = page.locator("div[data-testid='card-Lupo di Vapore']")

            await expect(custode_locator).to_be_visible()
            await expect(mirage_locator).to_be_visible()
            print("Both Custode and Mirage are available choices.")

            await custode_locator.click()
            print("Custode selected for sacrifice.")

            await expect(page.locator("div:text('Tocca a te.')")).to_be_visible(timeout=5000)
            print("Player turn has started, choice was processed.")

            await page.locator(".w-24 .pile").nth(1).click()
            await expect(page.locator(".bg-black\\/80 [data-testid='card-Custode del Velo']")).to_be_visible()
            print("Custode is in the graveyard.")
            await page.keyboard.press("Escape")

            player_field_locator = page.locator(".board-area").first()
            await expect(player_field_locator.locator("[data-testid='card-Lupo di Vapore']")).to_be_visible()
            print("Mirage is still on the field.")

            print("Test PASSED!")

        except Exception as e:
            print(f"Test FAILED: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
