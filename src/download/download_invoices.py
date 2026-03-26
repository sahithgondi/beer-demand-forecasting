import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

# load login from env
load_dotenv()

USERNAME = os.environ.get("SUPPLIER_USERNAME")
PASSWORD = os.environ.get("SUPPLIER_PASSWORD")

print("USERNAME loaded:", bool(USERNAME))
print("PASSWORD loaded:", bool(PASSWORD))
print("USERNAME value:", USERNAME)

# make sure the directory exists
DOWNLOAD_DIR = Path("data/downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def run():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            print("Attempting to log in...")

            page.goto(
                "https://b2biamgbnazprod.b2clogin.com/b2biamgbnazprod.onmicrosoft.com/oauth2/v2.0/authorize?p=b2c_1a_signin_signup_us&redirect_uri=https%3A%2F%2Fmybeesapp.com%2Fapi%2Fauth%2Fverify&response_type=id_token&response_mode=form_post&client_id=0d94d8f7-ff0f-41ce-b00e-e095aec22b5a&ui_locales=en-US&state=CUSTOMRj_wA_-Jb90sfgDS6hA4vLw9Wu30Kb4r%3Flanguage%3Den%26country%3DUS%26p%3DB2C_1A_SIGNIN_SIGNUP_US&nonce=bvc91igSDUuBK-y0lWBGBLG-W_HJOplU&scope=profile%20openid&x-client-SKU=passport-azure-ad&x-client-Ver=4.3.2",
                wait_until="domcontentloaded",
            )

            # first page email
            page.wait_for_selector("#signInName", state="visible", timeout=15000)
            print("Found username field")

            page.click("#signInName")
            page.wait_for_timeout(500)

            # clear any existing value
            page.press("#signInName", "Meta+A")
            page.press("#signInName", "Backspace")

            # type slowly to see username being filled
            page.type("#signInName", USERNAME, delay=100)
            page.wait_for_timeout(1000)

            typed_value = page.locator("#signInName").input_value()
            print("Typed username:", typed_value)

            if not typed_value:
                raise ValueError("Username was not entered into #signInName")

            page.screenshot(path="before_continue.png")

            # the visible button is continueNew not continue
            page.wait_for_selector("#continueNew", state="visible", timeout=15000)
            print("Found Continue button")
            page.locator("#continueNew").click()

            page.wait_for_timeout(3000)
            page.screenshot(path="after_continue.png")

            # sometimes it goes straight ot password other times it will ask for choice
            try:
                page.wait_for_selector("button.choice-form__choice", state="visible", timeout=5000)
                print("Password choice screen detected")
                page.locator("button.choice-form__choice").filter(has_text="Password").click()
            except TimeoutError:
                print("Password choice screen did not appear; checking for direct password page")

            # password page
            page.wait_for_selector("#password", state="visible", timeout=15000)
            print("Found password field")
            page.fill("#password", PASSWORD)

            password_value = page.locator("#password").input_value()
            print("Password entered:", bool(password_value))

            page.screenshot(path="before_login_click.png")

            # click Log In
            page.get_by_role("button", name="Log In").click()

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)

            print("Logged in")
            page.screenshot(path="logged_in_state.png")

            # continue download steps here

        except Exception as e:
            print(f"Automation failed: {e}")
            page.screenshot(path="error_capture.png")

        finally:
            print("Closing browser...")
            browser.close()


if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("Error: check SUPPLIER_USERNAME and SUPPLIER_PASSWORD in .env")
    else:
        run()