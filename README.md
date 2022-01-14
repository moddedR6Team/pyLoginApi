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
```
### Ubisoft
[POST] localhost:25565/api/ubisoft/


(Note: need to convert to base64 to made my job easier, but you can do any website with can encode base64)\
Headers:
```
B64: base64(email:pass)
email: email
password: password
```
# How to install/run?
```
pip install steam
pip install Flask
py api.py
```
