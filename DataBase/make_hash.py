import hashlib

def make_hash_from_str(data:str):
    md5_hash = hashlib.md5(data.encode())
    return md5_hash.hexdigest()

def make_id_for_user(username,password:str):
    res = ""
    for i in str(username)+str(password) :
         res += make_hash_from_str(i)

    return res
    

# print(make_hash_from_str("True")) # f827cf462f62848df37c5e1e94a4da74
# print(make_hash_from_str("False"))# f8320b26d30ab433c5a54546d21f414c

