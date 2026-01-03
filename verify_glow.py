
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000")

    # This card costs 3, the others sum to 3, so it should be playable
    hand_override = [
        {"name": "Mastro Stratega Leonhart", "strength": 3, "type": "Creatura", "rarity": "epic", "effect": "SCRY", "val": 1, "desc": "Quando entra, guarda la prima carta del mazzo; puoi metterla in fondo.", "faction": "human", "uid": "c1"},
        {"name": "Soldato della Muraglia", "strength": 1, "type": "Creatura", "rarity": "common", "effect": "NONE", "val": 0, "desc": "Nessuno.", "faction": "human", "uid": "c2"},
        {"name": "Picchiere della Milizia", "strength": 1, "type": "Creatura", "rarity": "common", "effect": "DEBUFF_ENEMY", "val": 1, "desc": "Quando entra, una creatura avversaria perde 1 Forza permanente.", "faction": "human", "uid": "c3"},
        {"name": "Recluta del Battaglione", "strength": 1, "type": "Creatura", "rarity": "common", "effect": "LOOT", "val": 1, "desc": "Quando entra, pesca 1 carta, poi scarta 1 carta.", "faction": "human", "uid": "c4"},
    ]

    page.evaluate("window.p1HandOverride = " + str(hand_override))
    page.evaluate("window.startingPlayerOverride = 1")

    page.click("text=UMANI")
    page.wait_for_selector('[data-testid="card-Mastro Stratega Leonhart"]')

    page.screenshot(path="playable_card_glow.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
