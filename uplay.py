import requests
import json
from requests.structures import CaseInsensitiveDict

url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"

url2 = "https://public-ubiservices.ubi.com/v1/profiles/me/gamesplayed"

rainbowPC = "5172a557-50b5-4665-b7db-e3f2e8c5041d"
rainbowPS4 = "05bfb3f7-6c21-4c42-be1f-97a33fb5cf66"
rainbowPS5 = "96c1d424-057e-4ff7-860b-6b9c9222bdbf"
rainbowXbox = "631d8095-c443-4e21-b301-4af1a0929c27"
rainbowXboxOne = "98a601e5-ca91-4440-b1c5-753f601a2c90"
rainbowStadia = "57e580a1-6383-4506-9509-10a390b7e2f1"

rainbowSixIDs = [rainbowPC,rainbowPS4,rainbowPS5,rainbowXbox,rainbowStadia]

def Uplay_Auth(b64):
      
    #Part1
    headers = CaseInsensitiveDict()
    headers["Ubi-AppId"] = "b8fde481-327d-4031-85ce-7c10a202a700"
    headers["GenomeId"] = "fbd6791c-a6c6-4206-a75e-77234080b87b"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Basic " + b64
    headers["Ubi-RequestedPlatformType"] = "uplay"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    data = '{"rememberMe": true}'
    req = requests.post(url, headers=headers,data=data)
    ## Posted to UBI, load to json
    json_data = json.loads(req.content)
    ticket = json_data["ticket"]
    name = json_data["nameOnPlatform"]
    exp = json_data["expiration"]
    sessionId = json_data["sessionId"]
    
    print(name)
    print(exp)
    
    #Part2
    headers2 = CaseInsensitiveDict()
    headers2["Ubi-AppId"] = "685a3038-2b04-47ee-9c5a-6403381a46aa"
    headers2["Content-Type"] = "application/json"
    headers2["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    headers2["Ubi-SessionId"] = sessionId
    headers2["Authorization"] = "Ubi_v1 t=" + ticket
    req2 = requests.get(url2, headers=headers2)
    json2 = json.loads(req2.content)
    
    # End
    # Checking if has r6
    hasr6 = False
    for played in json2["gamesPlayed"]:
          #print("spaceid " + played["spaceId"])
          if hasr6 is False:
            if played["spaceId"] in rainbowSixIDs:
                  print("Has R6!")
                  hasr6 = True
    
    return hasr6
