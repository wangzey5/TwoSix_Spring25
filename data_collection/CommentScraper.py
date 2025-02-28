"""
Utilities for scraping from regulations.gov

These utilities should generally not be interacted with directly, instead use `scrape.py`
"""

from playwright.sync_api import sync_playwright
import time
from copy import deepcopy
import numpy as np
import textract
import tempfile

def parse_attachment(attachment, extension):
    with tempfile.NamedTemporaryFile(delete=True) as temp:
        temp.write(attachment)
        temp.flush()
        text = textract.process(temp.name, extension=extension, encoding="utf-8").decode("utf-8")

    return text

class APICommentDetailScraper:
    def __init__(self, api, parseAttachments=True):
        self.parseAttachments = parseAttachments
        self.api = api

    def _get_comment_details(self, comment):
        """Request comment-specific data given a bulk comment response json object (eg; one sample from 'api.regulations.gov/v4/comments.data')"""
        return self.api.url(comment["links"]["self"]).get()

    def _get_attachment_text(self, comment_data):
        """Request attachment data for a specific comment"""
        attachments = self.api.url(comment_data["data"]["relationships"]["attachments"]["links"]['related']).get()
        attachment_text = []
        for attachment in attachments["data"]:
            attachment_format_urls = attachment["attributes"]["fileFormats"]
            attachment_formats = {}
            for attachment_format_url in attachment_format_urls:
                extension = attachment_format_url["format"]
                attachment = self.api.url(attachment_format_url["fileUrl"]).get(get_json=False).content
                try:
                    attachment_formats[extension] = parse_attachment(attachment, extension)
                except Exception as e:
                    print(f"Failed to parse filetype '{extension}' for attachment {attachment_format_url['fileUrl']}")
                    print(e)
            attachment_text.append(attachment_formats)
        return attachment_text
    
    def get_comment_details(self, comment):
        """Get and parse all relevant data for one entry of a bulk comment response"""
        comment_details = self._get_comment_details(comment)
        comment_atr = comment_details["data"]["attributes"]
        return {
            "response": comment_details,
            "comment": {
                "plaintext": comment_details["data"]["attributes"]["comment"],
                "attachments": self._get_attachment_text(comment_details) if self.parseAttachments else None
            },
            "documentId": comment_atr["commentOnDocumentId"],
            "docketId": comment_atr["docketId"],
            "title": comment_atr["title"],
            "agencyId": comment_atr["agencyId"]
        }

class PWCommentDetailScraper:
    def __init__(self, baseurl = "https://www.regulations.gov/") -> None:
        self.baseurl = baseurl
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch()

    def __del__(self):
        self.p.stop()

    def _get_plaintext(self, page):
        if not page.is_visible('xpath=//h2[text()="Comment"]/following-sibling::div'):
            return ""
        else:
            plaintext = page.locator('xpath=//h2[text()="Comment"]/following-sibling::div')
            try:
                return plaintext.text_content().strip()
            except:
                return ""

    def _get_attachment_text(self, page):
        attachments = [a.get_attribute("href") for a in page.locator('xpath=//h2[contains(text(), "Attachments")]/..//a[contains(@class, "btn")]').all()]
        return ""
        ## TODO 
        # Implement Attachments -> text

    def _get_hierarchy(self, page):
        page.locator('xpath=//section[@class="section-hierarchy"]').is_visible()
        return [h.get_attribute("href") for h in  page.locator('xpath=//section[@class="section-hierarchy"]//a').all()]

    def get_comment_details(self, comment):
        url = f"{typemap[comment["type"]]}/{comment["id"]}"
        page = self.browser.new_page()
        page.goto(self.baseurl + url)
        page.wait_for_timeout(2000)

        docketId, documentId = self._get_hierarchy(page)
        comment_details = {
            "id": comment["id"],
            "comment": {
                "plaintext": self._get_plaintext(page) 
            },
            "attachments": self._get_attachment_text(page),
            "documentId": documentId,
            "docketId": docketId,
            "title": "", ## TODO
            "agencyId": "" ## TODO
        }
        page.close()
        return comment_details

typemap = {
    "comments": "comment",
    "document": "document"
}

def insert(doc, collection):
    doc["_inserted_time"] = time.time()
    doc["_idx"] = collection.count_documents({})
    collection.insert_one(doc)

def exists(document, collection):
    return collection.count_documents({"id": document["id"]}, limit=1) != 0

def getAllComments(apibasereq, collection, checkpoint_collection):
    pageNum = 1
    metaPageNum = 1
    date = None
    if checkpoint_collection.countDocuments() > 0:
        date = checkpoint_collection.find()["lastmodifiedDate"]
        apibasereq.lastmodified(date)
    while True: 
        apireq = deepcopy(apibasereq)
        try:
            documents = apireq.sort("lastModifiedDate").page(pageNum).get()
            print(f"[{metaPageNum}](pg {pageNum}/20) ratelimit={apireq.ratelimit}", end="")
            print(" "*100, end="\r")
        except RuntimeError:
            print("Rate Limit exceeded, retrying in 1 minute")
            time.sleep(60)
            continue
        except ConnectionError as e:
            print(e)
            continue

        if len(documents["data"]) == 0:
            break

        for doc in documents["data"]:
            if exists(doc, collection):
                continue
            insert(doc, collection)

        if documents["meta"]["hasNextPage"] == False:
            if date is not None:
                checkpoint_collection.delete_one()
                checkpoint_collection.insert_one({"lastmodifiedDate": date})
            date = documents["data"][-1]["attributes"]["lastModifiedDate"]
            apibasereq.lastmodified(date)
            pageNum = 1
            metaPageNum += 1
        else:
            pageNum += 1


def getCommentDetails(scraper, comments, collection):
    i = 0
    while i<len(comments):
        comment = comments[i]
        if exists(comment, collection):
            continue
        try:
            comment_details = scraper.get_comment_details(comment)
        except RuntimeError:
            print("Rate Limit exceeded, retrying in 1 minute")
            time.sleep(60)
            continue

        insert(comment_details, collection)
        i+=1
