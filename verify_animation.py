import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:8000", wait_until="networkidle")

        await page.evaluate("""() => {
            window.p1HandOverride = [
                { name: "Soldato Semplice", strength: 0, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "...", faction: 'human', uid: 'test-card-play', animationId: 'human-anim-play', currentStrength: 0, tempStrength: 0 }
            ];
            window.p1FieldOverride = [];
            window.p1GraveOverride = [];
            window.p2FieldOverride = [{ name: "Nemico Dummy", strength: 1, type: 'Creatura', rarity: 'common', effect: 'NONE', val: 0, desc: "...", faction: 'beast', uid: 'enemy-dummy', animationId: 'enemy-dummy-1', currentStrength: 1, tempStrength: 0 }];
            window.startingPlayerOverride = 1;
        }""")

        await page.click('div.group:has-text("UMANI")')

        await page.wait_for_selector('[data-testid="card-Soldato Semplice"]', timeout=10000)
        await page.wait_for_timeout(1000)

        await page.click('[data-testid="card-Soldato Semplice"]')
        await page.wait_for_timeout(200)

        await page.click('button:has-text("GIOCA")')

        await page.wait_for_selector('.animating-card-container', state='visible', timeout=5000)
        await page.wait_for_timeout(250)

        await page.screenshot(path="/home/jules/verification/animation_verification.png")

        await browser.close()

asyncio.run(main())
