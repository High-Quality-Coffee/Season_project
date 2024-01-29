import re

userdb=wiz.model("orm").use("user")

db=struct.db("user_info")

def save():
    user={}
    user["id"]=wiz.request.query('id')
    user["name"]=wiz.request.query('name')
    user["email"]=wiz.request.query('email')
    user["phone"]=wiz.request.query('phone')
    user["interview"]=wiz.request.query('interview')

    db.update(userdb)

    

    return wiz.response.status(200, True)
    

