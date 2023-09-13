import json
import pandas as pd
import requests
import random
import datetime
import ctypes
import sys

print("***  Welcome to the 'Bulk create users' Server Setup  ***")
print("***  Similar to 'google.com' :)  ***")
server = input("Please enter the name of your server: ")
password = input("Please enter the password of your server: ")
account_name = []
print("***  Example: 'abbas'  ***")
account_name_msg = input("Please enter the desired account name:")
account_name.append(account_name_msg)
print("***  Example: '350', which will result in 'abbas350'  ***")
num_accounts = int(input("Please enter the number of accounts you want to create: "))
print("***  Example: If you want to create 30 accounts, enter '10'  ***")
num_retries = int(input("Please enter the total number of accounts you need: ")) 
print("***  Enter the number of days for which you want the account to be active. Example: '30'  ***")
many_days = int(input("Please enter the desired account validity period (in days):"))


date = datetime.datetime.now()
print(f'Today is {date.date()}')
ex_date = date + datetime.timedelta(days= int(many_days))
print(f'ExpireTime is {ex_date.date()}')

apisite = f"https://{server}:5555/api/"
password = "Abbas1368Abbas1369"

username = ""
def SendCommand(gateway, password, method, params):
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": "rpc_call_id",
            "method": method,
            "params": params
        }
        headers = {'content-type': 'application/json'}
        
        response = requests.request("POST", url=gateway, headers=headers, data=json.dumps(payload), 
                                    verify=True, auth=(username, password))
        data = response.json()
        return data['result']
    except:
        return False
       
def vhub():
    try:
        method = "EnumHub"
        params = {}
        p = SendCommand(apisite, password, method, params)
        response = pd.json_normalize(p, record_path =['HubList'])['HubName_str'].values[0]
        return response
    except:
        False
    
# userlist must be delete later and replaced by get_userlist()
userlist = []
def get_userlist():
    try:
        method = "EnumUser"
        params = {
            "HubName_str": vhub()
            }
        response = SendCommand(apisite, password, method, params)
        if isinstance(response, dict) and 'UserList' in response:
            response = pd.json_normalize(response['UserList'])['Name_str'].values
            for r in response:
                userlist.append(r)
        return userlist
    except:
        sys.exit(ctypes.windll.user32.MessageBoxW (0, "Error in getting server info you entered\n BE CAREFUL NEXT TIME.\n this is the END", "server error", 0))
get_userlist()   

def create_account(username,acc_password):
    try:
        VHub = vhub()
        method = "CreateUser"
        params = {
            "HubName_str": VHub,
            "Name_str": username,
            
            "ExpireTime_dt": str(ex_date.date())+'T11:30:36',
            "AuthType_u32": 1,
            "Auth_Password_str": acc_password,
            "UsePolicy_bool": True,
            "policy:Access_bool": True,
            "policy:MaxConnection_u32": 32,
            "policy:TimeOut_u32": 20,
            "policy:MultiLogins_u32": 1,
        }
        SendCommand(apisite, password, method, params)
        return f'{username} - {acc_password}'
    except:
        sys.exit(ctypes.windll.user32.MessageBoxW (0, "Error to Create Account", "error", 0))

    
def join_acc_name_num():
    final_result = "".join(account_name+[str(num_accounts)])
    return final_result  
print(f'Account Start as: {join_acc_name_num()}')

file = open("userlist.txt","a")
file.write(f'\n -------------- \n')
file.write(f'\n Name: {"".join(account_name)}')
file.write(f'\n ***Start as: {"".join(account_name+[str(num_accounts)])} ***')
file.write(f'\n server: {server}')
file.write(f'\n Create: {str(date.date())}')
file.write(f'\n Expired: {str(ex_date.date())}\n')


number = 1
while number <= int(num_retries):
    try:
        if join_acc_name_num() in userlist:
            error_acc_ex = ctypes.windll.user32.MessageBoxW (0, f'username {join_acc_name_num()} already exists Press ok to continue or Cancel to EXIT: ', "Already exists", 1)
            if error_acc_ex == True:
                num_accounts = num_accounts +1
            else:
                sys.exit(ctypes.windll.user32.MessageBoxW (0, "Check the Server and Try Again.\n i'm always here!. ", "SAD Ending", 0))
        else:
            clientname = join_acc_name_num()
            ACC_Password = str(random.randint(0,999999)).zfill(6)
            print(f'Trying To Create Acc: {join_acc_name_num()}')
            print(f'Acc Created: {create_account(clientname,ACC_Password)}')
            file.write(f'\n{create_account(clientname,ACC_Password)}')
            num_accounts = num_accounts +1
            number = number +1
        
    except:
        sys.exit(ctypes.windll.user32.MessageBoxW (0, "Something went wrong i don't know why", "error", 0))
           
print("BYE BYE ;)")
end = ctypes.windll.user32.MessageBoxW (0, "All account was create.\n EVETHING IS OK!.\n GOOD LUCK.\n Check the note. ", "THE END", 0)