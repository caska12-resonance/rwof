from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to the local server
    page.goto("http://localhost:8000")

    # Set up the game state
    page.evaluate("""() => {
        const humanDeck = [
            { name: "Picchiere della Milizia", strength: 1, type: 'Creatura', rarity: 'common', effect: 'DEBUFF_ENEMY', val: 1, desc: "Quando entra, una creatura avversaria perde 1 Forza permanente.", uid: 'c1' },
            { name: "Soldato della Muraglia", strength: 1, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "Nessuno.", uid: 'c2'},
            { name: "Soldato della Muraglia", strength: 1, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "Nessuno.", uid: 'c3'},
            { name: "Soldato della Muraglia", strength: 1, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "Nessuno.", uid: 'c4'},
            { name: "Soldato della Muraglia", strength: 1, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "Nessuno.", uid: 'c5'},
        ];
        const enemyCreature = { name: "Lupo Comune", strength: 1, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "-", uid: 'e1' };

        window.p1HandOverride = humanDeck;
        window.p2FieldOverride = [enemyCreature];
        window.startingPlayerOverride = 1;
    }""")

    # Start the game
    page.click("text=UMANI")
    time.sleep(1)

    # Play the card that requires a target
    page.click('[data-testid="card-Picchiere della Milizia"]')
    time.sleep(0.5)

    # Click the other cards in hand to pay for it
    page.click('[data-testid="card-Soldato della Muraglia"]')
    time.sleep(0.5)

    # Confirm the play
    page.click("text=GIOCA")
    time.sleep(1)

    # Take a screenshot
    page.screenshot(path="targetable_card_glow.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
