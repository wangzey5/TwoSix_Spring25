import argparse

from playwright.sync_api import sync_playwright

def makeKey(
    firstname="Emma",
    lastname="Fountain",
    email="randumbemma@gmail.com"
):
    baseurl = "https://open.gsa.gov/api/regulationsgov/"
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(baseurl)
    page.wait_for_timeout(2000)

    page.evaluate("() => window.scrollBy(0, 300)")

    page.get_by_label("First Name ").fill(firstname)
    page.get_by_label("Last Name ").fill(lastname)
    page.get_by_label("Email ").fill(email)
    page.get_by_text("I have read and agree to the terms and conditions.").check()
    page.get_by_role("button", name="Sign up").last.click()

    page.wait_for_timeout(2000)

    page.close()
    p.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="The number of keys to create")
    parser.add_argument("--name", help="First and last name, space separated")
    parser.add_argument("--email", help="Email to send API keys to")
    args = parser.parse_args()

    for i in range(args.n):
        first, last = args.name.split(" ")
        makeKey(first, last, args.email)
        print(f"Created {i+1}/{args.n}", end="")
        print(" "*100, end="\r")

