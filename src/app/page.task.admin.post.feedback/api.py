import re

db=wiz.model("orm").use("community")
feedback_db=wiz.model("orm").use("feedback")

def onLoad():
    email=wiz.request.query("user_email",True)

    where=dict(
        user_email=email,
        fields="title,writer,content,user_name"
    )

    rows=feedback_db.get(**where)
    wiz.response.status(200,rows)


    