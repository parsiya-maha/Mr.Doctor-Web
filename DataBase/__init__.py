from .make_hash import make_hash_from_str,make_id_for_user
from .check_login_data import check_login_data_in_json,islogin_json,change_islogin_json,how_is_login_json
from .log import find_last_id_json,add_log_json,change_one_value_in_json_data,find_index_from_id_json
from .log import delete_log_from_json_data,give_up_tabel_json_data_in_log,return_json_data_as_list,logout
from .signup import SignUp

#Defind instance var
path_users_data = r"App\DataBase\users.json"
path_system_data = r"App\DataBase\system.json"
path_log_data = r"App\DataBase\log.json"