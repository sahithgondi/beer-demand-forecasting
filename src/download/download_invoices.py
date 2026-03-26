import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# load credentials from env
load_dotenv()

USERNAME = os.environ.get("SUPPLIER_USERNAME")
PASSWORD = os.environ.get("SUPPLIER_PASSWORD")

print("USERNAME loaded:", bool(USERNAME))
print("PASSWORD loaded:", bool(PASSWORD))
print("USERNAME value:", USERNAME)

# make sure the download directory exists
DOWNLOAD_DIR = Path("data/downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def run():
    with sync_playwright() as p:
        # launch browser with headless=False so we can see what's happening
        print("Launching browser...")    
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            # username log in
            print("Attempting to log in...")
            page.goto("https://b2biamgbnazprod.b2clogin.com/b2biamgbnazprod.onmicrosoft.com/oauth2/v2.0/authorize?p=b2c_1a_signin_signup_us&redirect_uri=https%3A%2F%2Fmybeesapp.com%2Fapi%2Fauth%2Fverify&response_type=id_token&response_mode=form_post&client_id=0d94d8f7-ff0f-41ce-b00e-e095aec22b5a&ui_locales=en-US&state=CUSTOMRj_wA_-Jb90sfgDS6hA4vLw9Wu30Kb4r%3Flanguage%3Den%26country%3DUS%26p%3DB2C_1A_SIGNIN_SIGNUP_US&nonce=bvc91igSDUuBK-y0lWBGBLG-W_HJOplU&scope=profile%20openid&x-client-SKU=passport-azure-ad&x-client-Ver=4.3.2", wait_until="domcontentloaded")
            
            #first page log in
            page.wait_for_selector("#signInName", state="visible", timeout=10000)
            print("found user name field")
            page.fill("#signInName", USERNAME)
            page.wait_for_selector("#continueNew", state="visible", timeout=10000)
            page.locator("#continueNew").click()

            #select password button
            page.wait_for_selector("button.choice-form__choice", timeout=10000)
            page.locator("button.choice-form__choice").filter(has_text="Password").click()

            # enter password
            page.wait_for_selector("#password", timeout=10000)
            page.fill("#password", PASSWORD)
            page.get_by_text("Log In").click()

            page.wait_for_load_state("networkidle")
            print("Logged in!")


        except Exception as e:
            print(f"Automation failed: {e}")
            # Take a debugging screenshot whenever it crashes
            page.screenshot(path="error_capture.png")
            
        finally:
            print("Closing browser...")
            browser.close()

if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("error: check user and pass in env")
    else:
        run()
