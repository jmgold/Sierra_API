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
    header = {"Authorization": "Bearer " + token, "Content-Type": "application/json;charset=UTF-8"}
    request = requests.get("https://library.minlib.net:443/iii/sierra-api/v4/items/?limit=500&fields=bibIds%2Cstatus%2CcallNumber%2CupdatedDate&updatedDate=%5B{}T00%3A00%3A01Z%2C%5D&deleted=false&duedate=%5B{}T00%3A00%3A01Z%2C%5D&suppressed=false&locations=lex*".format(date.today() - timedelta(days=1),date.today() + timedelta(days=7)), headers = header)
    json_response = json.loads(request.text)
    return json_response
    

def main():
    my_list = new_checkouts() 
    with io.open('new_checkouts.html','w', encoding="utf-8") as f:
        f.write(json2html.convert(json = my_list))
    f.close() 

                  
main()

