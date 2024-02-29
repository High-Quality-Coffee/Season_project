import re
import season
import datetime
import json
import os

#user_info db 사용
userdb=wiz.model("orm").use("user_info")
db=wiz.model("orm").use("community")
reviewdb=wiz.model("orm").use("review")
assignmentdb=wiz.model("orm").use("assignment")

def assign():
    user=dict()
    review=dict()
    user["id"]=wiz.request.query('id', True)
    user["name"]=wiz.request.query('name', True)
    review["name"]=wiz.request.query('name', True)

    user["email"]=wiz.request.query('email', True)
    review["email"]=wiz.request.query('email', True)
    
    user["phone"]=wiz.request.query('phone', True)
    endPhoneNum=user["phone"][-4:] #휴대폰 번호 뒤 4자리
    user["assignName"]=wiz.request.query("assignName",True)
    word_list = user["assignName"].strip('[]').split(',')

    user["interview"]=wiz.request.query('interview', True)
    date_obj = datetime.datetime.fromisoformat(user["interview"])
    one_day_ago = date_obj - datetime.timedelta(days=1)
    one_day_ago_2359 = one_day_ago.replace(hour=23,minute=59)

    # Print the result in the same format
    user["duedate"]=one_day_ago_2359.strftime("%Y-%m-%d %H:%M")

    user["center"]=wiz.request.query('center', True)
    user["password"]='season'+endPhoneNum
    user["role"]="user"

    userdb.insert(user)
    reviewdb.insert(review)

    for word in word_list:
        user["title"]=word
        assignmentdb.insert(user)


    return wiz.response.status(200, True)


def onLoad():
    email=wiz.request.query("email",True)

    where=dict(
        fields="title"
    )

    rows=db.rows(**where)
    wiz.response.status(200,rows)
    
# def saveAssign():
#     user2=dict()
#     user2["assignName"]=wiz.request.query("assignName",True)
    
#     userdb.insert(user2)
#     wiz.response.status(200,True)

