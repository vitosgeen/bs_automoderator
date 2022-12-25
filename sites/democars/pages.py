
import base64
import os
import random
import cv2
import pytesseract
import imutils
import numpy as np
import argparse
import shutil, sys
from PIL import Image
from urllib.parse import urlparse
import urllib.request
from urllib.request import urlopen
import requests
import json
import urllib3

class Pages:

    # Const
    url_base = ""
    PAGE_LOGIN = "/user/login"
    PAGE_LOGIN_NAME = "admin"
    PAGE_LOGIN_PASS = "123"
    PAGE_MODERATOR = "/cars9custom/actionmoderator"
    PAGE_MODERATOR_ACCEPT = "/cars9custom/ActionModerated?accept=1"
    PAGE_MODERATOR_DECLINE = "/cars9custom/ActionModerated?decline=1"

    # Session
    session = requests.Session

    def __init__(self, name, passw):
        self.url_base = str(os.getenv('URL_BASE'))
        self.PAGE_LOGIN_NAME = name
        self.PAGE_LOGIN_PASS = passw
        
    def login(self):
        url = self.url_base + self.PAGE_LOGIN
        print(url)
        self.session = requests.Session()
        headers = self.headers()
        cookies = self.cookies()
        urllib3.disable_warnings()
        response = self.session.post(url, data={"name": self.PAGE_LOGIN_NAME, "pass": self.PAGE_LOGIN_PASS}, headers=headers, cookies=cookies, timeout=5, verify=False)   
        if response.status_code != requests.codes.ok:
            print("response.status_code not ok: ", response.status_code)
            return False

        print("response.status_code ok: ", response)
        return True
        
    def page_moderator(self, limit=10, offset=0):
        urllib3.disable_warnings()
        suffix = "?limit={}&offset={}".format(limit, offset)
        url = self.url_base + self.PAGE_MODERATOR + suffix
        self.session = requests.Session()
        response = self.session.get(url, verify=False)  
        if response.status_code != requests.codes.ok:
            print("page_moderator not ok: ", response.status_code)
            return False

        return response
        
    def page_accept(self, sk_id, ski_id):
        urllib3.disable_warnings()
        self.session = requests.Session()
        url = self.url_base + self.PAGE_MODERATOR_ACCEPT
        body = json.dumps({sk_id:{"search_keyword":{"id": sk_id}, "search_keyword_images":{ski_id: ski_id}}})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=body, verify=False)
        if response.status_code != requests.codes.ok:
            print("page_accept not ok: ", response.status_code)
            return False
        print("page_accept: ", sk_id, ski_id)
        return response.json()
        
    def page_decline(self, sk_id, ski_id):
        urllib3.disable_warnings()
        self.session = requests.Session()
        url = self.url_base + self.PAGE_MODERATOR_DECLINE
        body = json.dumps({sk_id:{"search_keyword":{"id": sk_id}, "search_keyword_images":{ski_id: ski_id}}})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=body, verify=False)
        if response.status_code != requests.codes.ok:
            print("page_decline not ok: ", response.status_code)
            return False

        print("page_decline: ", sk_id, ski_id)
        return response.json()

    def cookies(self):
        return {}
        
    def headers(self):
        headers = {
            'User-Agent': self.parser_get_user_agent(),
            'Content-Type': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def parser_get_user_agent(self):
        user_agent_list = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            ]
        return random.choice(user_agent_list)
        