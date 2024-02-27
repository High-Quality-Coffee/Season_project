import re

feedback_db=wiz.model("orm").use("feedback")

def onLoad():
    email=wiz.request.query("user_email",True)

    where=dict(
        user_email=email,
        fields="id,title,writer,created,user_name"
    )
    
    rows=feedback_db.rows(**where)
    wiz.response.status(200,rows)

    

