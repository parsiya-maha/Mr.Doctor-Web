# Import models
import json
import jmespath
import pandas as pd
from .check_login_data import how_is_login_json
from .make_hash import make_hash_from_str

#Defind instance var
path_users_data = r"App\DataBase\users.json"
path_system_data = r"App\DataBase\system.json"
path_log_data = r"App\DataBase\log.json"


# Find last id from log database
def find_last_id_json():

    with open(path_log_data) as F:
        data = json.load(F)

    ids = jmespath.search("[*].log_id",data)

    if ids == []:
        return 1
    
    return max(ids)


# Add log ro database
def add_log_json(log_id,_id,option,result,time,path,point):
    with open(path_log_data) as F:
        reader = json.load(F)

    reader.append({
        "log_id" : log_id,
        "id": _id,
        "option" : option,
        "result" : result,
        "time" : time,
        "path" : path,
        "point" : point
    })

    with open(path_log_data,"w") as F:
        json.dump(reader,F,indent=4)



# Change one value with [row,column] index in json file
def change_one_value_in_json_data(row,column,value):
    with open(path_log_data) as F:
        reader = json.load(F)

    key = list(reader[0].keys())[column]

    reader[row][key] = value

    with open(path_log_data,"w") as F:
        json.dump(reader,F,indent=4)



# Find index of log from id (log data)
def find_index_from_id_json(_id):
    with open(path_log_data) as F:
        reader = json.load(F)

    ids = jmespath.search("[*].log_id",reader)
    return ids.index(_id)


# Delete one log from data with id
def delete_log_from_json_data(_id):
    with open(path_log_data) as F:
        reader = json.load(F)

    ids = jmespath.search("[*].log_id",reader)
    index = ids.index(_id)

    reader.pop(index)

    with open(path_log_data,"w") as F:
        json.dump(reader,F,indent=4)


# Read data [log.csv] and return data as list
def return_json_data_as_list():
    how = how_is_login_json()

    if how == "f8320b26d30ab433c5a54546d21f414c" :
        ...

    else :
        with open(path_log_data) as F:
            reader = json.load(F)

        data = jmespath.search(f"[? id==`{how}`].[log_id,option,result,time,path,point]",reader)

        return data
    


# Return data of `info tabel` in log app :
#   Count    (len )
#   Point    (mean)
#   Time     (mean)
#   Option   (most)
#   Result   (most)

def give_up_tabel_json_data_in_log():

    data = return_json_data_as_list()

    df = pd.DataFrame(columns=["log_id","option","result","time","path","point"],index=list(range(len(data))))

    i = 0

    for item in data:
        df.iloc[i] = item
        i += 1




    n_sent = df.shape[0]

    if n_sent > 0:
        return [
                df["time"].count(),
                round(df["point"].apply(lambda x:float(x)).mean(),4),
                round(df["time"].apply(lambda x:float(x)).mean(),4),
                df["option"].mode()[0],
                df["result"].mode()[0]
            ]

    # When we dont have any log
    return ["nan","nan","nan","nan","nan"]


# Log out in app
def logout():
    with open(path_system_data) as F:
        reader = json.load(F)

    reader["login_status"] = make_hash_from_str("False")
    
    with open(path_system_data,"w") as F:
        json.dump(reader,F,indent=4)