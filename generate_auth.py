import asyncio
from playwright.async_api import async_playwright

async def generate_storage_state():
    async with async_playwright() as p:
        # Launch persistent context using local Chrome binary
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./chrome_user_data",
            channel="chrome",  # Uses your system's real Chrome
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        page = context.pages[0] if context.pages else await context.new_page()

        print("\n[+] Navigating to Google Colab...")
        await page.goto("https://colab.research.google.com")

        print("[!] ACTION REQUIRED: Log into your Google Account in the browser window.")
        print("[!] Waiting 90 seconds for you to log in...\n")
        await asyncio.sleep(90)

        # Export session state to JSON file
        await context.storage_state(path="google_auth.json")
        print("[✓] SUCCESS: google_auth.json created!")
        await context.close()

if __name__ == "__main__":
    asyncio.run(generate_storage_state())