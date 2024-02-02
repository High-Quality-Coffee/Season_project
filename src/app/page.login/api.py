import re

db = wiz.model("orm").use("user_info")

def login():
    email=wiz.request.query("email",True)
    password=wiz.request.query("password", True)
    user=db.get(email=email)
    

    if user is None:
        return wiz.response.status(401, "아이디를 확인해주세요")
    
    #if user["password"]!=password:
    #    wiz.response.status(401,"비밀번호를 확인해주세요")

    #이 코드는 왜 되는 걸까
    if user['password'](password) == False:
        return wiz.response.status(401, "비밀번호를 확인해주세요")

    if user['role'] == "admin":
        wiz.response.status(200,"admin")
    else:
        wiz.response.status(200,"user")

    