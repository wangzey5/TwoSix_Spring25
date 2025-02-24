import requests
import numpy as np
from datetime import datetime

class Reg_API:
    def __init__(
        self, 
        page_size=20, 
        apikey="e7LVpmbLfa0f0dDAx6TPzg86cG5TASGTafkxQHWg"
    ):
        self.apibase = "https://api.regulations.gov/v4"
        self.apikey = apikey
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

    def sort(self, field):
        self.reqstr = self.reqstr + f"&sort={field}"
        return self

    def lastmodified(self, date, mod="ge"):
        if isinstance(date, datetime):
            date = date.strftime("%Y-%m-%d %H:%M:%S")
        self.reqstr = self.reqstr + f"&filter[lastModifiedDate][{mod}]={date}"
        return self
        

    ### Get response(s)
    def get(self, get_json=True):
        response = requests.get(self.reqstr)
        if get_json:
            response = response.json()
        self.reqstr = ""
        return response
