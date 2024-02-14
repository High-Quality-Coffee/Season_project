import json

db=wiz.model("orm").use("community")
userdb=wiz.model("orm").use("user_info")

def onLoad():
    email=wiz.request.query("email",True)
    where=dict(
        email=email,
        fields="assignName,duedate"
    )

    rows=userdb.rows(**where)
    wiz.response.status(200,rows)


def onLoading():
    rowsArr=[];
    arys=wiz.request.query("list",True)
    arys=json.loads(arys)

    for ary in arys:
        rowsArr.append(db.get(title=ary))

    wiz.response.status(200,rowsArr)
