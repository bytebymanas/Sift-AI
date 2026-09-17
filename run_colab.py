import asyncio
import os
import sys
from playwright.async_api import async_playwright

COLAB_URL = os.getenv("COLAB_URL")
STORAGE_STATE = "google_auth.json"

async def execute_notebook():
    if not COLAB_URL:
        print("[X] FATAL ERROR: COLAB_URL environment variable is missing.")
        sys.exit(1)

    if not os.path.exists(STORAGE_STATE):
        print(f"[X] FATAL ERROR: {STORAGE_STATE} not found.")
        sys.exit(1)

    print("[+] Initializing Playwright browser instance...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        context = await browser.new_context(
            storage_state=STORAGE_STATE,
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            print(f"[+] Navigating to Colab: {COLAB_URL}")
            await page.goto(COLAB_URL, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)

            print(f"[+] Loaded Page Title: '{await page.title()}'")
            print(f"[+] Loaded Page URL: '{page.url}'")

            # Handle 'Choose an account' prompt if Google displays account picker
            if "accounts.google.com" in page.url or "signin" in page.url:
                print("[!] Google Account Choose screen detected. Attempting auto-select...")
                account_tile = page.locator("div[data-email], li:has-text('kukkadmasti@gmail.com')")
                if await account_tile.is_visible(timeout=5000):
                    await account_tile.click()
                    print("[+] Clicked account tile. Waiting for session redirect...")
                    await page.wait_for_load_state("networkidle", timeout=15000)

            # Check if still stuck on login screen
            if "accounts.google.com" in page.url:
                print("[X] ERROR: Session expired. Google requires password login.")
                await page.screenshot(path="failure.png")
                sys.exit(1)

            # Wait for Colab toolbar or notebook elements
            print("[+] Waiting for Colab interface elements...")
            try:
                await page.wait_for_selector("#menubar-container, colab-run-button, .notebook-container", timeout=45000)
                print("[+] Colab UI element detected successfully.")
            except Exception:
                print("[!] Specific selector not found, attempting direct shortcut trigger...")

            await asyncio.sleep(3)

            print("[+] Triggering 'Run All' cells (Ctrl+F9)...")
            await page.keyboard.press("Control+F9")

            # Handle untrusted notebook warning dialog if present
            try:
                run_anyway_btn = page.locator("paper-button:has-text('Run anyway'), mwc-button:has-text('Run anyway')")
                if await run_anyway_btn.is_visible(timeout=5000):
                    await run_anyway_btn.click()
                    print("[+] Handled 'Run anyway' modal dialog.")
            except Exception:
                pass

            print("[+] Workflow execution signal sent successfully.")
            print("[+] Holding runner for 12 minutes to complete CrewAI execution & email dispatch...")
            await asyncio.sleep(720)

            await browser.close()
            print("[✓] Process completed cleanly.")

        except Exception as e:
            print(f"[X] EXCEPTION: {e}")
            await page.screenshot(path="failure.png")
            await browser.close()
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(execute_notebook())