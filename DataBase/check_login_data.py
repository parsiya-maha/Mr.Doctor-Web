# Import models
import json
import jmespath
from .make_hash import make_hash_from_str

#Defind instance var
path_users_data = r"App\DataBase\users.json"
path_system_data = r"App\DataBase\system.json"
path_log_data = r"App\DataBase\log.json"


# Function to check login data [ username , password ]
def check_login_data_in_json(username:str,password:str):

    with open(path_users_data) as F:
        data = json.load(F)

    usernames = jmespath.search("[*].username",data)
    passwords = jmespath.search("[*].password",data)
    
    password = make_hash_from_str(password)

    for u,p in zip(usernames,passwords):
        if [username,password] == [u,p]:
            return True
        
    return False


# Function to said user was login or not
def islogin_json():

    with open(path_system_data) as F:
        reader = json.load(F)["login_status"]

    if not reader == "f8320b26d30ab433c5a54546d21f414c":
        return True
    
    return False



def change_islogin_json(_bool:bool,username:str):

    with open(path_system_data) as F:
        reader = json.load(F)
    print(_bool)
    if not _bool:
        reader["login_status"] = make_hash_from_str("False")
    else:
        with open(path_users_data) as F:
            user_data = json.load(F)

        for item in user_data:
            if item["username"] == username:

                reader["login_status"] = item["id"]
                break

    with open(path_system_data,"w") as F:
        json.dump(reader,F,indent=4)



        
# How is login now
def how_is_login_json():
    with open(path_system_data) as F:
        reader = json.load(F)

    return reader["login_status"]