import re
import datetime
orm = wiz.model('orm')

import datetime
orm = wiz.model('orm')

def load():
    title = wiz.request.query('title', True)
    row = orm.use('community').get(title=title)
    wiz.response.status(200, {
        "post": row
    })

def create():
    community_id = wiz.request.query('community_id', True)
    content = wiz.request.query('content', True)
    if len(content) == 0:
        wiz.response.status(403)
    data = dict()
    data['community_id'] = community_id
    data['user_id'] = wiz.session.get('id')
    data['content'] = content
    data['created'] = datetime.datetime.now()
    data['updated'] = datetime.datetime.now()
    orm.use('comment').insert(data)
    wiz.response.status(200)

def update():
    comment_id = wiz.request.query('id', True)
    content = wiz.request.query('content', True)
    user_id = wiz.session.get('id')
    if len(content) == 0:
        wiz.response.status(403)
    comment_db = orm.use('comment')
    # check = comment_db.get(id=comment_id, user_id=user_id)
    # if check is None and wiz.session.get('role') != 'admin':
    #     wiz.response.status(401)
    
    data = dict()
    data['content'] = content
    data['updated'] = datetime.datetime.now()
    comment_db.update(data, id=comment_id, user_id=user_id)
    wiz.response.status(200)

def delete():
    comment_id = wiz.request.query("id", True)
    comment_db = orm.use('comment')
    comment_db.delete(id=comment_id)
    wiz.response.status(200)

def comment():
    community_id = wiz.request.query('post_id', True)
    rows = orm.use('comment').rows(community_id=community_id, orderby="created", order="ASC")
    db = orm.use('user')
    for i in range(len(rows)):
        rows[i]['user'] = db.get(id=rows[i]['user_id'], fields="id,name")
        
    wiz.response.status(200, rows)



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


    