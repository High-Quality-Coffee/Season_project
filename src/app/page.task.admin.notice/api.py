import math

db=wiz.model("orm").use("community")

def search():
    page = int(wiz.request.query("page", True))
    category = wiz.request.query("category", True)
    dump = 14
    community_db = wiz.model('orm').use('community')

    where = dict(
        orderby="id",
        order="DESC",
        page=page,
        category=category,
        dump=dump
    )
    print(where)
    rows = community_db.rows(**where)
    lastpage = math.ceil(community_db.count(**where) / dump)

    for i in range(len(rows)):
        rows[i]['user'] = wiz.model('orm').use('user').get(id=rows[i]['user_id'], fields="id,name")
    
    wiz.response.status(200, {
        "list": rows,
        "lastpage": lastpage,
    })

def onLoaD():
    email=wiz.request.query("email",True)

    where=dict(
        fields="id,title"
    )

    rows=db.rows(**where)
    wiz.response.status(200,rows)
