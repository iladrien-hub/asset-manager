import json
import os
import re
from pprint import pprint

from bs4 import BeautifulSoup
from pip._vendor import requests


def load():
    r = requests.get("https://www.digminecraft.com/lists/item_id_list_pc.php")
    soup = BeautifulSoup(r.text, "html.parser")

    ids = [item.getText(strip=True).split(":")[-1][:-1] for item in soup.select("#minecraft_items tr td:nth-child(2)")]

    with open("./visualizer/assets/ids.json", "w", encoding="utf-8") as f:
        json.dump(ids, f)


def search():
    with open("./visualizer/assets/ids.json", encoding="utf-8") as f:
        ids = json.load(f)

    stairs = [item for item in ids if item.endswith("trapdoor")]
    res = {}
    for stair in stairs:
        res[stair] = "trapdoor"

    pprint(res)


if __name__ == '__main__':
    search()