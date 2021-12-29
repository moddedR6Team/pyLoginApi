from steam.client import SteamClient
from steam.enums import EResult
from steam.exceptions import SteamError

async def pass_stuff(uname,pwd,code,is2fa,codetype):
    client = SteamClient()
    
    
    @client.on("connected")
    @client.on(client.EVENT_CONNECTED)
    async def handle_connected():
        print("Connected to %s", client.current_server_addr)

    @client.on("reconnect")
    @client.on(client.EVENT_RECONNECT)
    async def handle_reconnect(delay):
        print("Reconnect in %ds...", delay)

    @client.on('error')
    @client.on(client.EVENT_ERROR)
    async def error(result):
        print("Logon result:", repr(result))
            
    @client.on('auth_code_required')
    @client.on(client.EVENT_AUTH_CODE_REQUIRED)
    async def auth_code(is_2fa):
        if is_2fa:
            print("2FA Code")
            client.login(two_factor_code=code,username=uname,password=pwd,login_id=1337)
        else:
            print("Email Code")
            client.login(auth_code=code,username=uname,password=pwd,login_id=1337)

        
    try:
        codex = False
        is2fa = is2fa.lower()
        codetype = codetype.lower()
        if is2fa=="yes":
            if codetype=="email":
                codex = False
                res = client.login(auth_code=code,username=uname,password=pwd,login_id=1337)
            if codetype=="code":
                codex = True
                res = client.login(two_factor_code=code,username=uname,password=pwd,login_id=1337)
        else:
            res = client.login(username=uname,password=pwd,login_id=1337)
        
        if client.EVENT_AUTH_CODE_REQUIRED:
            await auth_code(codex)
        
        if client.EVENT_ERROR:
            await error(res)
        
        if client.EVENT_CONNECTED:
            await handle_connected()
        
        
        if client.EVENT_CONNECTED:
            print("Logged on as:", client.user.name)
            #response = client.licenses[359550]
            #result = client.get_product_info(apps=[359550])
            tokens = client.get_access_tokens(app_ids=[359550])
            print(tokens)
            #print(result)
            """
            if result['apps'][359550]['_missing_token']:
                print(result)

                result = client.get_product_info(apps=[{'appid': 359550,
                                                'access_token': tokens['apps'][359550]
                                                }])
                print(result)
                print("_missing_token is true")
                print("Not Has R6!")
                return "Not has R6:S"
            else:
                print("Has R6:S!")
            """
            #print(response)
            client.logout()
            return "Successful " + tokens
        else:
            return "Something not right!"
    except SteamError as exp:
        print(exp.eresult,exp.message)
        return exp.eresult
    except:
        print("oh no")
        return "Something got failed!"
    
    
