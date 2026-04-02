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
        
        # spoof a chrome user agent
        context = browser.new_context(
            accept_downloads=True,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("Attempting to log in...")

            page.goto(
                "https://b2biamgbnazprod.b2clogin.com/b2biamgbnazprod.onmicrosoft.com/oauth2/v2.0/authorize?p=b2c_1a_signin_signup_us&redirect_uri=https%3A%2F%2Fmybeesapp.com%2Fapi%2Fauth%2Fverify&response_type=id_token&response_mode=form_post&client_id=0d94d8f7-ff0f-41ce-b00e-e095aec22b5a&ui_locales=en-US&state=CUSTOMRj_wA_-Jb90sfgDS6hA4vLw9Wu30Kb4r%3Flanguage%3Den%26country%3DUS%26p%3DB2C_1A_SIGNIN_SIGNUP_US&nonce=bvc91igSDUuBK-y0lWBGBLG-W_HJOplU&scope=profile%20openid&x-client-SKU=passport-azure-ad&x-client-Ver=4.3.2",
                wait_until="domcontentloaded",
            )

            # first page email
            page.wait_for_selector("#signInName", state="visible")
            print("Found username field")

            page.click("#signInName")

            # clear any existing value
            page.press("#signInName", "Meta+A")
            page.press("#signInName", "Backspace")

            # type slowly to see username being filled
            # nevermind no delay
            page.type("#signInName", USERNAME)

            typed_value = page.locator("#signInName").input_value()
            print("Typed username:", typed_value)

            if not typed_value:
                raise ValueError("Username was not entered into #signInName")

            page.screenshot(path="before_continue.png")

            # button is not continue
            page.wait_for_selector("#continueNew", state="visible")
            print("Found Continue button")
            page.locator("#continueNew").click()

            page.screenshot(path="after_continue.png")

            # sometimes it goes straight ot password other times it will ask for choice
            try:
                page.wait_for_selector("button.choice-form__choice", state="visible", timeout=5000)
                print("Password choice screen detected")
                page.locator("button.choice-form__choice").filter(has_text="Password").click()
            except TimeoutError:
                print("Password choice screen did not appear; checking for direct password page")

            # password page
            page.wait_for_selector("#password", state="visible")
            print("Found password field")
            page.fill("#password", PASSWORD)

            password_value = page.locator("#password").input_value()
            print("Password entered:", bool(password_value))

            page.screenshot(path="before_login_click.png")

            # click log in
            page.get_by_role("button", name="Log In").click()

            print("Waiting for redirect to the intermediate page...")
            
            # wait for it to route back to home page
            page.wait_for_url("https://mybeesapp.com/")
            
            print("Clicking the secondary 'Log In' button...")
            page.wait_for_selector("text='Log In'", state="visible")
            page.locator("text='Log In'").first.click()

            # wait for invoices text on header
            # page.wait_for_selector("text='Invoices'", state="visible")
            
        #    page.locator("a.bees-link-wrapper[href='/invoices']").first.click()

            page.goto("https://mybeesapp.com/invoices")
            print("Sucessfully got to invoices page")
            
            """
            print("Waiting for the Invoices link to become visible...")
            # exvlude the footer links and and only select the one visible
            invoices_link = page.locator("a.bees-link-wrapper[href='/invoices']:not([target='_blank']):visible")
            
            # page.get_by_text("Invoices").first.click()
            # if there is still a race condition then wait for this to be visible
            invoices_link.wait_for(state="visible")
            invoices_link.click()

            print("Clicked invoices")

            print("Logged in successfully!")
            print("This is the url after login:", page.url)
            """
            page.screenshot(path="logged_in_state.png")
            
            # Use wait_for_timeout to wait a split second (1000 milliseconds = 1 second)
            page.wait_for_timeout(100)
            
            page.wait_for_selector("text='All Invoices'").click()
            print("Selected All Invoices...")
            
            # Wait another split second before looking for table rows
            page.wait_for_timeout(100)
            
            # wait until tr in tbody appears in the page DOM
            first_row = page.locator("tbody tr").first
            print("Found first row")

            # inside first row find the first span with the class and then get its visible text. then strip
            amount_locator = first_row.locator("span.bees-number-display").first
            
            amount_locator.wait_for(state="visible", timeout=60000)
            # get the text and clean it
            amount_text = amount_locator.inner_text().strip()
            # cleans the string and convert to float
            amount = float(amount_text.replace(",", "").replace("$", ""))

            print("Amount text:", amount_text)
            
            # if amount > 200 then click the button
            if amount > 200:
                first_row.locator("button:has(svg[data-icon-name='EyeOn'])").click()
                print("Clicked View Details for most recent invoice...")
            else:
                print("Most recent invoice total is not above 200, so we are skipping.")
                
            # keep script open until i close it
            input("Press Enter to close the browser...")
        
            





        except Exception as e:
            print(f"Automation failed: {e}")
            page.screenshot(path="error_capture.png")
            # input("Browser is paused AFTER ERROR for debugging. Inspect the page, then press Enter to close...")
"""
        finally:
            print("Closing browser...")
            browser.close()
"""

if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("Error: check SUPPLIER_USERNAME and SUPPLIER_PASSWORD in .env")
    else:
        run()