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
        print(f"[X] FATAL ERROR: Storage state file '{STORAGE_STATE}' not found.")
        sys.exit(1)

    print("[+] Initializing Playwright browser instance...")
    async with async_playwright() as p:
        # Launch headless Chromium with security flags
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        
        # Load authenticated Google context
        context = await browser.new_context(storage_state=STORAGE_STATE)
        page = await context.new_page()

        print(f"[+] Navigating to Google Colab: {COLAB_URL}")
        await page.goto(COLAB_URL, wait_until="networkidle")

        # Wait for interface initialization
        print("[+] Waiting for Colab interface to load...")
        await page.wait_for_selector("#menubar-container", timeout=60000)

        # Trigger execution (Ctrl + F9)
        print("[+] Colab ready. Pressing Ctrl+F9 ('Run All')...")
        await page.keyboard.press("Control+F9")

        # Bypass untrusted notebook dialog if prompt appears
        try:
            run_anyway_btn = page.locator("paper-button:has-text('Run anyway')")
            if await run_anyway_btn.is_visible(timeout=5000):
                await run_anyway_btn.click()
                print("[+] Handled 'Run anyway' modal dialog.")
        except Exception:
            pass

        # Execution hold window (12 minutes) for CrewAI execution + email dispatch
        print("[+] Agentic workflow execution initiated successfully.")
        print("[+] Holding execution window open for 12 minutes...")
        await asyncio.sleep(720)

        await browser.close()
        print("[✓] Execution finished cleanly. Shutting down cloud runner.")

if __name__ == "__main__":
    asyncio.run(execute_notebook())