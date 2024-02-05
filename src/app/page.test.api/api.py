import re

db=wiz.model("orm").use("user_info")

def test():
    userName=wiz.request.query("name", True)
    
    data=wiz.model('orm').use('user').get(name=userName)

    wiz.response.status(200,data)

def data():
    user=dict()
    user['center']=wiz.request.query('center',True)

    get = db.get(center=user['center'],fields="name,center,email")
    print(get)
    wiz.response.status(200,get)
