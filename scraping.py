import requests
import numpy as np
from pdf2image import convert_from_bytes
import pytesseract
import os
from dotenv import load_dotenv

class Reg_API:
    def __init__(self, page_size=20):
        load_dotenv()
        self.apibase = "https://api.regulations.gov/v4"
        self.apikey = os.getenv("API_KEY")
        self.page_size = page_size
        self.reqstr = ""

    def _add_apikey(self):
        self.reqstr = self.reqstr + f"?api_key={self.apikey}"
        return self

    ### Main url constructors
    def endpoint(self, endpoint):
        self.reqstr = f"{self.apibase}{endpoint}"
        self._add_apikey()
        return self

    def url(self, url):
        self.reqstr = url
        self._add_apikey()
        return self

    ### Search modifiers
    def search(self, search_term):
        self.reqstr = self.reqstr + f"&filter[searchTerm]={search_term}"
        return self

    def page(self, page):
        self.reqstr = self.reqstr + f"&page[size]={self.page_size}&page[number]={page}"
        return self

    ### Get response(s)
    def get(self, get_json=True):
        response = requests.get(self.reqstr)
        if get_json:
            response = response.json()
        self.reqstr = ""
        return response

# Parse pdf bytes to get text
def parse_pdf(pdf):
    imgs = convert_from_bytes(pdf)
    text = ""
    for img in imgs:
        text = text + pytesseract.image_to_string(np.array(img))
    return text

class CommentParser:
    def __init__(self, api):
        self.api = api

    def _get_comment_info(self, comment):
        """Request comment-specific data given a bulk comment response json object (eg; one sample from 'api.regulations.gov/v4/comments.data')"""
        return self.api.url(comment["links"]["self"]).get()

    def _get_attachments(self, comment_data):
        """Request attachment data for a specific comment"""
        return self.api.url(comment_data["data"]["relationships"]["attachments"]["links"]['related']).get()
    
    def _get_comment_text(self, comment_info, attachments):
        """Parse out text-comment from comment json and parse any attachments"""
        plaintext_comment = comment_info["data"]["attributes"]["comment"]
        attachment_comments = []
        for attachment in attachments["data"]:
            attachment_format_urls = attachment["attributes"]["fileFormats"]
            attachment_formats = {}
            for attachment_format_url in attachment_format_urls:
                extension = attachment_format_url["fileUrl"].split(".")[-1]
                if extension == "pdf":
                    attachment_formats["pdf"] = parse_pdf(self.api.url(attachment_format_url["fileUrl"]).get(get_json=False).content)
                else:
                    print(f"Failed to parse filetype '{extension}' for attachment {attachment_format_url['fileUrl']}")
            attachment_comments.append(attachment_formats)
    
        return {
            "plaintext": plaintext_comment,
            "attachments": attachment_comments
        }
    
    def get_comment_data(self, comment):
        """Get and parse all relevant data for one entry of a bulk comment response"""
        comment_info = self._get_comment_info(comment)
        attachments = self._get_attachments(comment_info)
        return {
            "_id": comment["id"], # use response comment ID as mongodb Primary Key _id
            "comment_response": comment,
            "comment_info": comment_info,
            "attachments": attachments,
            "comment_text": self._get_comment_text(comment_info, attachments)
        }
