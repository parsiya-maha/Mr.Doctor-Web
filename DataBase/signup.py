# Import models
import re
import json
import jmespath
from CTkMessagebox import CTkMessagebox
import customtkinter
from .make_hash import make_hash_from_str,make_id_for_user



#Defind instance var
path_users_data = r"App\DataBase\users.json"
path_system_data = r"App\DataBase\system.json"
path_log_data = r"App\DataBase\log.json"


# Class for sign up methods
class SignUp :
    
    @staticmethod
    def email_valid(email:str):
        pattern = r".{2,20}@gmail.com"
        res = re.findall(pattern,email)

        if res == []:
            return False
        
        return True


    @staticmethod
    def username_vaid(username:str):
        with open(path_users_data) as F:
            reader = json.load(F)

        usernames = jmespath.search("[*].username",reader)

        return username not in usernames
    

    @staticmethod
    def show_massage_box(sms:str):
        CTkMessagebox(message=sms,
                  title="Mr.Doctor - Signup",
                  icon="cancel", option_1="Try again")


    @staticmethod
    def signup_in_app_json(
        fname:str,
        lname:str,
        username:str,
        email:str,
        password:str,
        rpassword:str
    ):
        
        # fname = en_fname.get()
        # lname = en_lname.get()
        # username = en_username.get()
        # email = en_email.get()
        # password = en_password.get()
        # rpassword = en_rpassword.get()
        
        if fname == "" :
            return "First name field is empty !"

        
        if lname == "" :
            return "Last name field is empty !"


        if username == "" :
            return "The username field is empty !"


        if not SignUp.username_vaid(username) :
            return "This username exists in the system."


        if not SignUp.email_valid(email) :
            return "The email is invalid !"


        if password == "":
            return "The password field is empty !"


        if password != rpassword :
            return "The retry password is not equal with correct password"
        
        with open(path_users_data) as F:
            reader = json.load(F)

        reader.append({
            "id" : make_id_for_user(username,password),
            "username" : username,
            "password" : make_hash_from_str(password)
        })

        with open(path_users_data,"w") as F:
            json.dump(reader,F,indent=4)


        with open(path_system_data) as F:
            reader = json.load(F)

        reader["login_status"] = make_id_for_user(username,password)

        with open(path_system_data,"w") as F:
            json.dump(reader,F,indent=4)

        return True




