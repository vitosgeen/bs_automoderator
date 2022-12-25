import datetime
import glob
import random
import string
import sys
import time
import unittest
import os
import cv2
import pytesseract
import datetime
from bs4 import BeautifulSoup
from PIL import Image
from utils import Utils
from sites.democars import pages
import conf



def start_moderation(limit, offset):
    p = pages.Pages("admin", "123")
    p.login()
    response_mpage = p.page_moderator(limit, offset)
    if not response_mpage:
        print("Something went wrong: page moderator not has not loaded")
        return False
    parsing_moderation(p, response_mpage)
    return True

def parsing_moderation(spages, response):
    items = get_items(response.text)
    u = Utils.Utils()
    u.remove_dir_images()
    u.create_dir_images()
    iterations = 0
    total_iterations = 0
    total_texts = 0
    total_humans = 0
    total_faces = 0
    total_nocars = 0
    iterations_len = len(items)
    for item in items:
        time.sleep(1)
        xtotal = total_texts + total_humans + total_faces + total_nocars
        print("================","i:", total_iterations, "========", iterations, " : ", iterations_len, "========", datetime.datetime.now())
        print("========", xtotal, "========", "Texts:", total_texts, "=== Humans:", total_humans, "=== Faces:", total_faces, "=== NoCars:", total_nocars)
        total_iterations += 1
        iterations += 1
        path_image = u.download_image(imgurl=item['img_orig_src'])
        if not path_image:
            continue
        vimg = u.validate_image(path_image)
        if vimg == None:
            continue
        
        textstr = u.detect_text(path_image)
        if (len(textstr) > 3):
            print("detect TEXT: " + textstr)
            spages.page_decline(item["sk_id"], item["ski_id"])
            total_texts += 1
            continue

        persons = u.detect_humans(path_image)
        if (persons > 0):
            print("detect HUMANS: " + str(persons))
            spages.page_decline(item["sk_id"], item["ski_id"])
            total_humans += 1
            continue

        faces = u.detect_faces(path_image)
        if (faces > 0):
            print("detect FACES: " + str(faces))
            spages.page_decline(item["sk_id"], item["ski_id"])
            total_faces += 1
            continue

        cars = u.detect_vehicles(path_image)
        if (cars < 1):
            print("NO detect CARS: " + str(cars))
            spages.page_decline(item["sk_id"], item["ski_id"])
            total_nocars += 1
            continue

        spages.page_accept(item["sk_id"], item["ski_id"])

def get_items(response_text):
    soup = BeautifulSoup(response_text, 'lxml')
    elements = soup.select(".cars9 div.row-images div.item-image")
    items = []
    for el in elements:
        item = {}
        ski_id = el.find_all("input")[0]["value"]
        sk_id = el.find_all("input")[0]["sk-id"]
        item['ski_id'] = ski_id
        item['sk_id'] = sk_id
        item['img_src'] = el.find_all("img")[0]["data-src"]
        item['img_orig_src'] = el["data-orig"]        
        items.append(item)
    return items

n = len(sys.argv)
limit_arg = sys.argv[1]
offset_arg = sys.argv[2]
conf.load_dotenv()
start_time = datetime.datetime.now().timestamp()
for x in range(1000):
    x = start_moderation(limit_arg, offset_arg)
    if not x:
        break
    end_time = datetime.datetime.now().timestamp()
    print("Time iterations: ", (end_time - start_time))
    if (end_time - start_time) > 1500:
        break