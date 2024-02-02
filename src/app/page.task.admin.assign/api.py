import re

#user_info db 사용
userdb=wiz.model("orm").use("user_info")


def assign():
    user=dict()
    user["id"]=wiz.request.query('id', True)
    user["name"]=wiz.request.query('name', True)
    user["email"]=wiz.request.query('email', True)
    user["phone"]=wiz.request.query('phone', True)
    endPhoneNum=user["phone"][-4:] #휴대폰 번호 뒤 4자리
    
    user["interview"]=wiz.request.query('interview', True)
    user["center"]=wiz.request.query('center', True)
    user["password"]='season'+endPhoneNum
    user["role"]="user"
    
    userdb.insert(user)

    return wiz.response.status(200, True)
    

