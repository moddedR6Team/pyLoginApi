import sqlite3
con = sqlite3.connect('api.db')
import os
import dotenv

dotenv.load_dotenv()

def search_user(username):
    cursor = con.execute('''SELECT NAME from API WHERE IS_USED LIKE "0" AND IS_EXP LIKE "0" AND NAME LIKE ''' + '"' + username + '"')
    usesrfound = 0
    for row in cursor:
        if row[0] != "":
            usesrfound+=1
        print(row[0])
    x = True
    if usesrfound != 0: 
        x = True 
    else: 
        x = False
    return x

def search_token(token):
    cursor = con.execute('''SELECT NAME from API WHERE IS_USED LIKE "0" AND IS_EXP LIKE "0" AND TOKEN LIKE ''' + '"' + token + '"')
    tokenfnd = 0
    for row in cursor:
        if row[0] != "":
            tokenfnd+=1
        print(row[0])
    x = True
    if tokenfnd != 0: 
        x = True 
    else: 
        x = False
    return x

def add_user(username,token):
    if search_user(username) == False:
        con.execute("INSERT INTO API (NAME,TOKEN,IS_USED,IS_EXP) VALUES ('" + username + "','" + token + "',False,False)");
        con.commit()
    else:
        print(username + " is already added")
    return True

def set_token_used(username,token):
    con.execute("UPDATE API set IS_USED = 1 where TOKEN = '" + token + "' AND NAME = '" + username + "'");
    con.commit()
    return True

def set_token_exp(username,token):
    con.execute("UPDATE API set IS_EXP = 1 where TOKEN = '" + token + "' AND NAME = '" + username + "'");
    con.commit()
    return True

def create():
    con.execute('''CREATE TABLE IF NOT EXISTS API
         (ID INTEGER NOT NULL,
         NAME           TEXT    NOT NULL,
         TOKEN           TEXT     NOT NULL,
         IS_USED           BOOL     NOT NULL,
         IS_EXP           BOOL     NOT NULL,
         PRIMARY KEY("ID" AUTOINCREMENT)
         );''')
    con.commit()

def close():
    con.close()
    return True