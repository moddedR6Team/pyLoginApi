# Python Login API
Python (Steam/Uplay) Login API with Steam(ValvePython)/Uplay and Flask

To get you have R6:S POST to Localhost:25565 (Port can be edited!)
Note:\
If you want to use this to production or elsewhere you should edit the port to something else.\
And obviously the localhost is will be your IP.\
Also Flask ask you to dont use that stuff on production, I have no idea how to make that safe, so have fun 😎

### Steam
[POST] localhost:25565/api/steam/

Headers:
```
has2fa: yes/no
codetype: email/code
username: uname
password: upassw
code: codefrommail
token: serialsecret
```
### Ubisoft
[POST] localhost:25565/api/ubisoft/


(Note: need to convert to base64 to made my job easier, but you can do any website with can encode base64)\
Headers:
```
B64: base64(email:pass)
email: email
password: password
token: serialsecret
```

### Status
[GET] localhost:25565/status/


### Verify
[POST] localhost:25565/verify/
```
name: email or uname that your created a token,logged in
token: serialsecret
```

### Used
[POST] localhost:25565/used/
```
name: email or uname that your created a token,logged in
token: serialsecret
```

# How to install/run?
```
pip install steam
pip install Flask
pip install pyjwt
py api.py
```
