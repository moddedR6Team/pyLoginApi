from flask import Flask
from flask import request
from flask import make_response
from markupsafe import escape
import steam_backend

app = Flask("SteamTest")
dec = ""
namelen = 6

@app.route('/')
def home():
	return "SlejmUr Test (API) Server ALIVE!\n" + "/api/enc or /api/dec"

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
async def token():
    uname = request.headers.get('username')
    pwd = request.headers.get('password')
    is2fa = request.headers.get('has2fa')
    code = request.headers.get('code')
    codetype = request.headers.get('codetype')
    if request.method == 'POST':
        resp = await steam_backend.pass_stuff(uname,pwd,code,is2fa,codetype)
        rsp = make_response(resp)
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
