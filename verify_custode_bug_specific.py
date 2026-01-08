
import asyncio
import re
import json
from playwright.sync_api import sync_playwright, expect

def run_test(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 720})
    page = context.new_page()

    custode_card = {"name": "Custode del Velo", "strength": 4, "type": "Creatura", "rarity": "epic", "effect": "PROTECT_MIRAGE_ONCE", "val": 0, "desc": "Una volta per partita...", "faction": "arcanum", "uid": "custode", "currentStrength": 4, "tempStrength": 0}
    mirage_card = {"name": "Drago di Vetro", "strength": 6, "type": "Creatura", "rarity": "epic", "effect": "MIRAGE", "val": 0, "desc": "Miraggio.", "faction": "arcanum", "uid": "mirage", "currentStrength": 6, "tempStrength": 0}

    # This card has strength >= 3 and an effect that destroys a Mirage
    destroyer_card = {"name": "Re Aldren, Giudizio della Corona", "strength": 4, "type": "Creatura", "rarity": "unique", "effect": "DESTROY_WEAK", "val": 6, "desc": "Quando entra, distruggi una creatura avversaria con Forza ≤6.", "faction": "human", "uid": "destroyer", "currentStrength": 4, "tempStrength": 0}
    payment_card = {"name": "Soldato della Muraglia", "strength": 1, "type": "Creatura", "rarity": "common", "effect": "NONE", "val": 0, "desc": "Nessuno.", "faction": "human", "uid": "payment", "currentStrength": 1, "tempStrength": 0}

    p1_field_override = [custode_card, mirage_card]
    p2_hand_override = [destroyer_card] + [{**payment_card, 'uid': f'p{i}'} for i in range(4)]

    try:
        page.goto("http://localhost:8000")

        page.evaluate(f"""() => {{
            window.p1FieldOverride = {json.dumps(p1_field_override)};
            window.p2HandOverride = {json.dumps(p2_hand_override)};
            window.startingPlayerOverride = 2; // AI goes first
        }}""")

        page.click("text=CONCLAVE ARCANA")
        print("Game started. AI's turn.")

        # Wait for AI to play and for the effect to trigger
        page.wait_for_timeout(3000)

        # The Mirage should still be on the field, but we expect this to fail
        mirage_on_field = page.locator("[data-testid='card-Drago di Vetro']")
        expect(mirage_on_field).to_be_visible()
        print("Mirage card is still visible on the field.")

        print("\n❌ Test Passed Unexpectedly: The bug was not reproduced. 'Custode del Velo' seems to be working.")


    except Exception as e:
        print(f"\n✅ Test Failed as Expected: The bug is present. The Mirage was likely destroyed.")
        print(f"   Error: {e}")
        page.screenshot(path="verify_custode_bug_specific_error.png")
        print("   Error screenshot saved.")


    finally:
        browser.close()

with sync_playwright() as p:
    run_test(p)
