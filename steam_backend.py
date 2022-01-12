from steam.client import SteamClient
from steam.exceptions import SteamError

import gevent.monkey
gevent.monkey.patch_all()

class SteamWorker(object):
    def __init__(self):
        
        self.steam = client = SteamClient()
        client.set_credential_location(".")

        @client.on("error")
        def handle_error(result):
            print("Logon result: ", repr(result))

        @client.on("channel_secured")
        def send_login():
            if self.steam.relogin_available:
                self.steam.relogin()
                
        @client.on("connected")
        def handle_connected():
            print("Connected to ", client.current_server_addr)

        @client.on("logged_on")
        def handle_after_logon():

            print("-"*30)
            print("Logged on as:", client.user.name)
            print("Community profile:", client.steam_id.community_url)
            print("Last logon:", client.user.last_logon)
            print("Last logoff:", client.user.last_logoff)
            print("-"*30)

        @client.on("disconnected")
        def handle_disconnect():
            print("Disconnected.")


        @client.on("reconnect")
        def handle_reconnect(delay):
            print("Reconnect in: ", delay)

    def prompt_login(self):
        self.steam.cli_login()

    def close(self):
        if self.steam.logged_on:
            print("Logout")
            self.steam.logout()
        if self.steam.connected:
            self.steam.disconnect()

    def get_has_r6(self):
        tokens = self.steam.get_access_tokens(app_ids=[359550])
        result = self.steam.get_product_info(apps=[{'appid': 359550,
                                                'access_token': tokens['apps'][359550]
                                                }])
        print("Tokens: " + str(tokens))
        print("missingtoken: " + str(result['apps'][359550]['_missing_token']))
        return not bool(result['apps'][359550]['_missing_token']) #this will flip to if this false , give back true. And vica versa
    
    def login(self,uname,pwd):
        print("Login")
        result = self.steam.login(username=uname,password=pwd,login_id=1337)
        return result
    
    def login2fa(self,uname,pwd,code,codetype):
        print("Login with 2FA")
        if codetype == "email":
            print("Email Code")
            result = self.steam.login(auth_code=code,username=uname,password=pwd,login_id=1337)
            return result
        if codetype == "code":
            print("2FA Code")
            result = self.steam.login(two_factor_code=code,username=uname,password=pwd,login_id=1337) 
            return result
