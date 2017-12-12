import requests
import json
import os
import io
from json2html import *
from datetime import date, timedelta


def get_token():
    url = "https://library.minlib.net/iii/sierra-api/v4/token"
    header = {"Authorization": "Basic T2tPZm1XT005UkloVXpMeWc5QkN6YUppVUdJTTpSdWZ1c2QwZw==", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    json_response = json.loads(response.text)
    token = json_response["access_token"]
    return token

def new_books():    
    token = get_token()
    header = {"Authorization": "Bearer " + token, "Content-Type": "application/json;charset=UTF-8"}
    request = requests.get("https://library.minlib.net:443/iii/sierra-api/v4/bibs/?fields=id%2Ctitle%2Cauthor%2CmaterialType&createdDate=%5B{}T00%3A00%3A01Z%2C%5D&deleted=false&suppressed=false".format(date.today() - timedelta(days=3)), headers = header)
##    json_response = json.loads(request.content.decode('utf-8'))
    json_response = json.loads(request.text)
    return json_response
    

def main():
    my_list = new_books()
## delete matType code    
    for entry in my_list["entries"]:
        del entry["materialType"]["code"]
## test response
##    for k, v in my_list.items():
##        print('{0}:{1}'.format(k, v))
##change record number to Encore link
    for record in my_list["entries"]:
        record["id"] = "<a href=\"http://find.minlib.net/iii/encore/record/C__Rb" + record["id"] + " \">" + record["id"] + "</a>"
    with io.open('new_books.html','w', encoding="utf-8") as f:
        f.write(json2html.convert(json = my_list))
    f.close() 

                  
main()
