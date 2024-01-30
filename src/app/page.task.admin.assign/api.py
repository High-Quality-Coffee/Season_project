import re

userdb=wiz.model("portal/season/orm").use("user")


def save():
    user={}
    user["id"]=wiz.request.query('id', True)
    user["name"]=wiz.request.query('name', True)
    user["email"]=wiz.request.query('email', True)
    user["phone"]=wiz.request.query('phone', True)
    user["interview"]=wiz.request.query('interview', True)
    
    userdb.insert(user)

    return wiz.response.status(200, True)
    

