import requests
from requests.structures import CaseInsensitiveDict
import json

url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"

#685a3038-2b04-47ee-9c5a-6403381a46aa
#f35adcb5-1911-440c-b1c9-48fdc1701c68

#487091d6-a285-471c-9036-d4bce349f212
#5b36b900-65d8-47f3-93c8-86bdaa48ab50
"""
from requests.structures import CaseInsensitiveDict

url = ""

headers = CaseInsensitiveDict()
headers["Ubi-AppId"] = "685a3038-2b04-47ee-9c5a-6403381a46aa"
headers["GenomeId"] = "487091d6-a285-471c-9036-d4bce349f212"
headers["Content-Type"] = "application/json"
headers["Authorization"] = "Basic " + b64
headers["Ubi-RequestedPlatformType"] = "uplay "
"""

def get_ubiv1(b64):
  #b64 = basic64(email+ ":" + pass)
    headers = CaseInsensitiveDict()
    headers["Ubi-AppId"] = "685a3038-2b04-47ee-9c5a-6403381a46aa"
    headers["GenomeId"] = "487091d6-a285-471c-9036-d4bce349f212"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Basic " + b64
    headers["Ubi-RequestedPlatformType"] = "uplay"
    data = '{"rememberMe": true}'
    r = requests.post(url, headers=headers,data=data)
    print(r.content) # it print the full request to backend , need to be on try-catch(except)
    return "Yey"
