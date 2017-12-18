import requests
import json
import os
import io
from json2html import *
from datetime import date, timedelta

#insert apikey in line 11
def get_token():
    url = "https://library.minlib.net/iii/sierra-api/v4/token"
    header = {"Authorization": "Basic [myAPIKey]", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    json_response = json.loads(response.text)
    token = json_response["access_token"]
    return token

def new_checkouts():    
    token = get_token()
    url = "https://library.minlib.net/iii/sierra-api/v4/items/query?offset=0&limit=500"
    header = {"Authorization": "Bearer " + token, "Content-Type": "application/json;charset=UTF-8"}
    query = {"queries": [{"target": {"record": {"type": "item"},"id": 63},"expr": {"op": "equals","operands": ["12-15-2017",""]}},"and",{"target": {"record": {"type": "item"},"id": 87},"expr": {"op": "between","operands": ["178","188"]}},"or",{"target": {"record": {"type": "item"},"id": 87},"expr": {"op": "between","operands": ["645","653"]}}]}
    request = requests.post(url, data=json.dumps(query), headers = header)
    convert_request = json.loads(request.text)
    return convert_request
    
def get_bibIds(item_list):
    token = get_token()
    id_string = ""
    header = {"Authorization": "Bearer " + token, "Content-Type": "application/json;charset=UTF-8"}	
    for entry in item_list["entries"]:
        try:
            id_string +=("%2C" + entry["link"].split("items/",1)[1])
        except KeyError:
            continue
    id_string = id_string[3:]
    request = requests.get("https://library.minlib.net:443/iii/sierra-api/v4/items/?id={}&fields=bibIds".format(id_string), headers = header)
    convert_request = json.loads(request.text)
    return convert_request
		
def get_title(bibs):
    token = get_token()
    header = {"Authorization": "Bearer " + token, "Content-Type": "application/json;charset=UTF-8"}
    id_string =""
    for entry in bibs["entries"]:
        try:
            id_string +=("%2C" + entry["bibIds"][0])
        except KeyError:
            continue
    id_string = id_string[3:]
    request = requests.get("https://library.minlib.net:443/iii/sierra-api/v4/bibs/?limit=500&offset=0&id={}&fields=title%2Cauthor".format(id_string), headers = header)
    convert_request = json.loads(request.text)
    return convert_request
    
def encore_link(titles):
    for record in titles["entries"]:
        record["title"] = "<a href=\"http://find.minlib.net/iii/encore/record/C__Rb" + record["id"] + " \">" + record["title"] + "</a>"
        del record["id"]
    return titles
    
def main():
    my_list = new_checkouts()
    bibs = get_bibIds(my_list)
    titles = get_title(bibs)
    titles = encore_link(titles)
    with io.open('lex_new_checkouts.html','w', encoding="utf-8") as f:
      f.write(json2html.convert(json = titles))
    f.close()
                    
main()

