from flask import Flask
from flask import request
from flask import make_response
import steam_backend
import uplay
import os
import gevent.monkey
import base64
import db
import jwt_lib
gevent.monkey.patch_all()

app = Flask("pyAPI")
dec = ""
namelen = 6

@app.route('/')
def home():
	return "SlejmUr Test (API) Server ALIVE!"


@app.route('/api/steam/',methods = ['GET', 'POST'])
def steam():
    uname = request.headers.get('username')
    pwd = request.headers.get('password')
    is2fa = request.headers.get('has2fa')
    if is2fa is None:
      is2fa = "no"
    code = request.headers.get('code')
    codetype = request.headers.get('codetype')
    token = request.headers.get('token')
    if jwt_lib.SERIAL_KEY_SECRET == token:
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
            if strep == True:
              toDb(uname,jwt_lib.generatetoken(uname))
          #resp = steam_backend.pass_stuff(uname,pwd,code,is2fa,codetype)
          rsp = make_response(strep)
          os.remove(uname + "_sentry.bin")
          return rsp
      if request.method == 'GET':
          rsp = make_response("Use POST method!")
          return rsp
    else:
      response = "Serial key is corrupt!"
      resp = make_response(str(response))
      return resp

@app.route('/api/ubisoft/',methods = ['GET', 'POST']) # implement ubisoft auth
def ubisoft():
  b64 = request.headers.get('B64')
  email = request.headers.get('email')
  password = request.headers.get('password')
  token = request.headers.get('token')
  if jwt_lib.SERIAL_KEY_SECRET == token:
    data = email + ":"  + password
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    if b64 is None:
      b64 = encodedStr
    if request.method == 'POST':
        response = uplay.Uplay_Auth(b64)
        if response == True:
          toDb(email,jwt_lib.generatetoken(email))
        resp = make_response(response)
        return resp
    if request.method == 'GET':
          rsp = make_response("Use POST method!")
          return rsp
  else:
    response = "Serial key is corrupt!"
    resp = make_response(str(response))
    return resp
      
@app.route('/api/verify/',methods = ['POST'])
def verify():
    uname = request.headers.get('username')
    token = request.headers.get('token')
    if jwt_lib.SERIAL_KEY_SECRET == token:
      accesstoken = request.headers.get('access_token')
      accesstoken = base64.b64decode(accesstoken)
      response = jwt_lib.verify_jwt(uname,accesstoken)
    else:
      response = "Serial key is corrupt!"
    resp = make_response(str(response))
    return resp

@app.route('/api/used/',methods = ['POST'])
def apidb():
    uname = request.headers.get('username')
    token = request.headers.get('token')
    if jwt_lib.SERIAL_KEY_SECRET == token:
      accesstoken = request.headers.get('access_token')
      accesstoken = base64.b64decode(accesstoken)
      response = db.set_token_used(uname,accesstoken)
    else:
      response = "Serial key is corrupt!"
    resp = make_response(str(response))
    return resp

def toDb(uname,token):
      response = base64.b64encode(token['access_token'].encode("utf-8"))
      response = str(response)
      response = response.replace("b'","")
      response = response.replace("'","")
      db.add_user(uname,token)

@app.route('/api/db/test/',methods = ['POST'])
def test():
    uname = request.headers.get('username')
    token = request.headers.get('token')
    accesstoken = request.headers.get('access_token')
    if jwt_lib.SERIAL_KEY_SECRET == token:
      toDb(uname,accesstoken)
    else:
      response = "Serial key is corrupt!"
    resp = make_response(str(response))
    return resp
      

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
     
db.create()  
run()
