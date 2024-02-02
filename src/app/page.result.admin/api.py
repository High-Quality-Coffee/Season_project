import re

db=wiz.model("orm").use("user_info")

def search():
    var="dev"
    category=wiz.request.query("category",True)
    rows=db.get(center=var)
    wiz.response.status(200,{
        "list" : rows
    })
