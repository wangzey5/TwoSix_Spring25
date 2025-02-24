from playwright.sync_api import sync_playwright
import time
import numpy as np

class Scraper:
    def __init__(self, baseurl = "https://www.regulations.gov/") -> None:
        self.baseurl = baseurl
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch()

    def __del__(self):
        self.p.stop()

    def getComment(self, url):
        page = self.browser.new_page()
        page.goto(self.baseurl + url)
        page.wait_for_timeout(2000)

        page.locator('xpath=//section[@class="section-hierarchy"]').is_visible()
        hierarchy = [h.get_attribute("href") for h in  page.locator('xpath=//section[@class="section-hierarchy"]//a').all()]

        if not page.is_visible('xpath=//h2[text()="Comment"]/following-sibling::div'):
            comment = ""
        else:
            comment = page.locator('xpath=//h2[text()="Comment"]/following-sibling::div')
            try:
                comment = comment.text_content().strip()
            except:
                comment = ""
        attachments = [a.get_attribute("href") for a in page.locator('xpath=//h2[contains(text(), "Attachments")]/..//a[contains(@class, "btn")]').all()]
        page.close()
        return {
            "comment": comment,
            "attachments": attachments,
            "hierarchy": hierarchy[::-1]
        }

typemap = {
    "comments": "comment",
    "document": "document"
}

if __name__ == "__main__":
    import pymongo
    db = pymongo.MongoClient().regulationsgov
    comments_c = db.comments

    testc = comments_c.find().next()

    scraper = Scraper()

    times = []
    comments = comments_c.find().limit(30)
    comment = comments.next()
    print(comment["_inserted_time"])
    for comment in comments:
        comment_url = f"{typemap[comment["type"]]}/{comment["id"]}"
        try:
            start = time.time()
            details = scraper.getComment(comment_url)
            comments_c.update_one({"_id": comment["id"]}, {"$set": details})
            times.append(time.time() - start)
        except:
            print(f"failed to scrape {comment_url}")
    print(comment["_inserted_time"])
    print(f"{sum(times)=}, {np.mean(times)=}")
