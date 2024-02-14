import re

db=wiz.model("orm").use("user_info")

def search():
    var="dev"
    center=wiz.request.query("center",True)

    where=dict(
        center=center,
        fields="name,center,email"
    )

    rows=db.rows(**where)
    wiz.response.status(200,rows)
