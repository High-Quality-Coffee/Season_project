import re

db=wiz.model("orm").use("community")

def onLoad():
    num=wiz.request.query("title",True)

    # where=dict(
    #     title=num,
    #     fields="id,title,content"
    # )

    # rows는 객체를 감싼 배열형태로 값을 return 해줌.
    # rows=db.rows(**where)

    rows=db.get(title=num, fields="id,title,content")

    print(rows)
    wiz.response.status(200,rows)


    