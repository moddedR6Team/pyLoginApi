# Python Login API
Python (Steam/Uplay) Login API with Steam(ValvePython)/Uplay and Flask

To get you have R6:S POST to Localhost:25565 (Port can be edited!)

### Steam:
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
# How to install/run?
```
pip install steam
pip install Flask
pip install pyjwt
py api.py
```

# Todo
Need to do:
- In /api/used/ point to check jwttoken before we make it to used
- remove test cases
