import requests
import json
import os
import io
from json2html import *
from datetime import date, timedelta

##enter token in line 11
def get_token():
    url = "https://library.minlib.net/iii/sierra-api/v4/token"
    header = {"Authorization": "[my_token]", "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    json_response = json.loads(response.text)
    token = json_response["access_token"]
    return token

def new_books():    
    token = get_token()
    header = {"Authorization": "Bearer " + token, "Content-Type": "application/json;charset=UTF-8"}
    request = requests.get("https://library.minlib.net:443/iii/sierra-api/v4/bibs/?fields=id%2Ctitle%2Cauthor%2CmaterialType&createdDate=%5B{}T00%3A00%3A01Z%2C%5D&deleted=false&suppressed=false".format(date.today() - timedelta(days=3)), headers = header)
    json_response = json.loads(request.text)
    return json_response
    

def main():
    book_list = new_books()
	
    for record in book_list["entries"]:
        print("RECORD: b" + record["id"] + "a \n")
        print("TITLE: " + record["title"] + "\n")
        print("AUTHOR: " + record["author"] + "\n")
        print("MATTYPE: " + record["materialType"]['value'] + "\n")

my_list = new_books() 
with io.open('new_books.html','w', encoding="utf-8") as f:
    f.write(json2html.convert(json = my_list))
f.close()           
##print(json2html.convert(json = my_list))          
##main()

