import re

db=wiz.model("orm").use("user_info")
reviewdb=wiz.model("orm").use("review")

def search():
    #center=wiz.request.query("center",True)
    
    where=dict(
        #center=center,
        fields="name,center,email,score"
    )

    rows=db.rows(**where)
    wiz.response.status(200,rows)


def category():
    center = wiz.request.query("category",True)

    where=dict(
        center=center,
        fields="name,center,email,score"
    )

    rows=db.rows(**where)
    wiz.response.status(200,rows)
    
    
def save():
    email=wiz.request.query("email_obj",True)
    score=wiz.request.query("score_obj",True)

    review=dict()
    review["score"]=score
    
    #comment_db.update(data, id=comment_id, user_id=user_id)

    reviewdb.update(review, email=email)
    db.update(review,email=email)
    wiz.response.status(200,True)


