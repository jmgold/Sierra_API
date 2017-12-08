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
    json_response = json.loads(request.content.decode('utf-8'))
    return json_response
    

def main():
    my_list = new_books()
## test response
    for k, v in my_list.items():
        print('{0}:{1}'.format(k, v))
##failed attempt to delete mattype code
    for k in my_list.items():
        if k == 'code':
            del my_list[k]    
##change record number to Encore link
    for record in my_list["entries"]:
        record["id"] = "http://find.minlib.net/iii/encore/record/C__Rb" + record["id"]
    with io.open('new_books.html','w', encoding="utf-8") as f:
        f.write(json2html.convert(json = my_list))
    f.close() 

                  
main()
