import re

db=wiz.model("orm").use("user_info")

def search():
    email=wiz.request.query("email",True)

    where=dict(
        email=email,
        fields="name,phone,center,interview,email"
    )

    rows=db.rows(**where)
    print(rows)
    wiz.response.status(200,rows)