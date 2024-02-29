import re
import season
import json
import os
import datetime

db=wiz.model("orm").use("community")
user_db=wiz.model("orm").use("user_info")
model = wiz.model('orm').use('user_info')
feedback_db=wiz.model("orm").use("feedback")

def onLoad():
    email=wiz.request.query("user_email",True)

    name=user_db.get(email=email).name

    print(name)
    wiz.response.status(200,name)


def load():
    id = wiz.request.query('id',True)
    row = model.get(id=id)
    wiz.response.status(200, row)
    
def update():
    data = json.loads(wiz.request.query('data', True))
    data['user_name']=user_db.get(email=data['user_email']).name
    data['user_id'] = wiz.session.get('id')
    data['updated'] = datetime.datetime.now()
    if data['id'] == '':
        del data['id']
        data['created'] = datetime.datetime.now()
        db_a=feedback_db.orm
        db_a.create(**data)
    else:
        row = model.get(id=data["id"])
        model.update(data, id=data['id'])
    
    files = wiz.request.files()
    for item in files:
        fs = season.util.os.FileSystem(os.path.join(storagepath, data["category"], str(data["id"])))
        fs.write.file(item.filename, item)

    
    wiz.response.status(200, True)
    
def delete():
    data_id = wiz.request.query('id', True)
    model.delete(id=data_id)
    wiz.response.status(200, True)

def delete_file(wiz):
    id = wiz.request.query("id",True)
    item = wiz.request.query("item",True)
    data = model.get(id=id)
    data["files"].remove(item)
    data['updated'] = datetime.datetime.now()
    model.update(data, id=id)
    wiz.response.status(200, True)

def save():
    user=dict()
    user["title"]=wiz.request.query('title',True)
    user["content"]=wiz.request.query('content',True)

    current_datetime =datetime.datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    user["created"]=current_date

    db.insert(user)
    wiz.response.status(200,True)


def feedback_save():
    feedback=dict()
    feedback["title"]=wiz.request.query("title",True)
    feedback["content"]=wiz.request.query("content",True)
    feedback["writer"]=wiz.request.query("writer",True)
    
    feedback["created"]=datetime.datetime.now()
    feedback["user_name"]=wiz.request.query("user_name",True)
    feedback["user_email"]=wiz.request.query("user_email",True)

    feedback_db.insert(feedback)
    wiz.response.status(200,True)
    