#!/usr/bin/python

import requests
import re
import pathlib
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.request
import shutil
import os
from bs4 import BeautifulSoup

s = requests.Session()
f = open(str(pathlib.Path(__file__).parent.resolve())+ "/config.json")
config = json.loads(f.read())
f.close()
print("Starting download.")

def getPostString(response, session):
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    a = soup.find_all("input")

    params = {}

    for tag in a:
        if tag.get("name") == "login":
            
            params[tag.get("name")] = os.environ["XLOGIN"]
        elif tag.get("name") == "password":
            params[tag.get("name")] = os.environ["PASSWD"]
        else:
            params[tag.get("name")] = tag.get("value")
    return(params)

def casLogin(response, session):
    body = getPostString(response, session)
    res = session.post(config["casAuthURL"], headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}, data=body, allow_redirects=False)
    if (res.status_code == 302) | (res.status_code == 301):
        res = session.get(res.headers["Location"], allow_redirects=False)
        if (res.status_code == 302) | (res.status_code == 301):
            return res.headers["Location"]
        else:
            raise IOError("Takeing cosign cookie to service's server failed")    
    else:
        raise IOError("Login failed")

def getPages(url, session):
    response = session.get(url)
    domain = urlparse(response.url).netloc
    if domain == config["casDomain"]:
        response = casLogin(response, session)
        response = session.get(response)
    return response

def getTargets():
    idList = []
    toGet = []
    for x in config["targets"]:
        response = getPages(x, s)
        page = response.content
        soup = BeautifulSoup(page, "html.parser", from_encoding="iso-8859-2")
        nadpis = soup.find("h1", {"class": "nadpis"})
        content = nadpis.parent
        content.find("ul")
        content = content.find_all("li")
        result = exportLink(content, s, idList)
        toGet.append(result["urlsToDownload"])
        idList = result["idList"]
    syncFolder(toGet, config["path"])
    if os.path.exists(config["path"] + "data.json"):
        os.remove(config["path"] + "data.json")
    with open(config["path"] + "data.json", 'w') as data:
        json.dump(toGet, data)


def syncFolder(listSync, path):
    path = path + "video/"
    toList = os.listdir(path)
    for element in toList:
        isnin = True
        for x in listSync:
            for y in x:
                if element.rsplit(".", 1)[0] == y["id"]:
                    isnin = False
                    break
        if isnin:
            os.remove(path + element)
    for x in listSync:
        for y in x:
            if y["id"] + config["ext"] not in toList:
                downloadVideo(y["url"], y["id"] + config["ext"], path)

def exportLink(content, session, idList):
    urlsToDownload = []
    x=len(content) - 1
    while ((-(x - len(content))) < int(os.environ["TODWN"])+1)&(x >= 0):
        i = len(content)
        url = content[x].find("a")
        predmet = (url.find("b").decode_contents())
        prednaska = (url.parent.find("div").decode_contents())
        url = url.attrs["href"]
        response = getPages(config["recordId"] + url, session)
        page = response.content
        soup = BeautifulSoup(page, "html.parser", from_encoding="iso-8859-2")
        a = soup.find("a", {"title":"Stažení záznamu"}).attrs["href"]
        id = parse_qs(urlparse(a).query)["id"][0]
        x -= 1
        urlsToDownload.append({"predmet": predmet,"prednaska":prednaska,"id": id, "url":a})
        idList.append(id)
    return {"idList": idList, "urlsToDownload": urlsToDownload}

def downloadVideo(url, filename, path):
    print("downloading: " + filename)
    path = os.sep.join([path, filename])
    s = requests.Session()
    response = s.get(url)
    location = casLogin(response, s)
    #pipe = urllib.request.urlopen()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(s.cookies))
    urllib.request.install_opener(opener)
    with urllib.request.urlopen(url) as response:
        if os.path.exists(path):
            os.remove(path)
        with open(path, "w+b") as f:
            shutil.copyfileobj(response, f)



#downloadVideo('https://video4.fit.vutbr.cz/av/record-download.php?id=63844', "test")

getTargets()
print("Finished download")