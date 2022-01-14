from flask import Flask
from flask import request
from flask import make_response
import steam_backend
import uplay
import os
import gevent.monkey
import base64
gevent.monkey.patch_all()

app = Flask("pyAPI")
dec = ""
namelen = 6

@app.route('/')
def home():
	return "SlejmUr Test (API) Server ALIVE!\n" #+ "/api/enc or /api/dec"


@app.route('/api/steam/',methods = ['GET', 'POST'])
def steam():
    uname = request.headers.get('username')
    pwd = request.headers.get('password')
    is2fa = request.headers.get('has2fa')
    if is2fa is None:
      is2fa = "no"
    code = request.headers.get('code')
    codetype = request.headers.get('codetype')
    if request.method == 'POST':
        worker = steam_backend.SteamWorker()
        if is2fa == "no":    
          resp = worker.login(uname,pwd)
        else:
          resp = worker.login2fa(uname,pwd,code,codetype)   
        print(resp)
        strep = str(resp)
        strep = strep.replace("<","")
        strep = strep.replace(">","")
        strep = strep.replace(":"," -")
        strep = strep.replace("EResult.","")
        if strep == "OK":
          strep = worker.get_has_r6()
        #resp = steam_backend.pass_stuff(uname,pwd,code,is2fa,codetype)
        rsp = make_response(strep)
        os.remove(uname + "_sentry.bin")
        return rsp
    if request.method == 'GET':
        rsp = make_response("Use POST method!")
        return rsp

@app.route('/api/ubisoft/',methods = ['GET', 'POST']) # implement ubisoft auth
def ubisoft():
  b64 = request.headers.get('B64')
  email = request.headers.get('email')
  password = request.headers.get('password')
  data = email + ":"  + password
  encodedBytes = base64.b64encode(data.encode("utf-8"))
  encodedStr = str(encodedBytes, "utf-8")
  if b64 is None:
    b64 = encodedStr
  if request.method == 'POST':
      response = uplay.Uplay_Auth(b64)
      resp = make_response(response)
      return resp
  if request.method == 'GET':
        rsp = make_response("Use POST method!")
        return rsp
      
@app.errorhandler(404)
def not_found(error):
    resp = make_response("ERROR 404", 404)
    resp.headers["Is-Error"] = "404"
    return resp

@app.errorhandler(500)
def error_500(error):
    resp = make_response("ERROR 500", 500)
    resp.headers["Is-Error"] = "500"
    return resp

def run():
  app.run(host='0.0.0.0', port=25565)
        
run()
