import requests
import numpy as np
from pdf2image import convert_from_bytes
import pytesseract

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
