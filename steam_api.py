from flask import Flask
from flask import request
from flask import make_response
import steam_backend
import gevent.monkey
gevent.monkey.patch_all()

app = Flask("SteamTest")
dec = ""
namelen = 6

@app.route('/')
def home():
	return "SlejmUr Test (API) Server ALIVE!\n" #+ "/api/enc or /api/dec"

"""
@app.route('/api/token/')
def token():
  b64 = request.headers.get('B64')
  if b64 is not None:
    response = ubi.get_ubiv1(b64)
    resp = make_response(response)
    return resp

@app.route("/api/download/<name>")
def api_download(name):
  resp = make_response(f"download {escape(name)}!")
  resp.headers["Is-Error"] = "None"
  resp.headers["Data"] = name
  return resp
"""
@app.route('/api/steam2fa/',methods = ['GET', 'POST'])
def token():
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
        
        return rsp
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
