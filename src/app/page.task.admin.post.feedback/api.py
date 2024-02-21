import re

db=wiz.model("orm").use("community")
feedback_db=wiz.model("orm").use("feedback")

def onLoad():
    email=wiz.request.query("user_email",True)
    title=wiz.request.query("fdb_title",True)

    where=dict(
        user_email=email,
        title=title,
        fields="title,writer,content,user_name"
    )

    rows=feedback_db.get(**where)
    wiz.response.status(200,rows)


    