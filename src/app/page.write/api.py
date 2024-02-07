import season
import json
import os
import datetime

storagepath = wiz.config("config").STORAGE_PATH
model = wiz.model('orm').use('community')
db=wiz.model('orm').use('community')

def load():
    id = wiz.request.query('id',True)
    row = model.get(id=id)
    wiz.response.status(200, row)
    
def update():
    data = json.loads(wiz.request.query('data', True))
    data['user_id'] = wiz.session.get('id')
    data['updated'] = datetime.datetime.now()
    if data['id'] == '':
        del data['id']
        data['created'] = datetime.datetime.now()
        db = model.orm
        data['id'] = db.create(**data)
    else:
        row = model.get(id=data["id"])
        model.update(data, id=data['id'])
    
    files = wiz.request.files()
    for item in files:
        fs = season.util.os.FileSystem(os.path.join(storagepath, data["category"], str(data["id"])))
        fs.write.file(item.filename, item)

    wiz.response.status(200, data['id'])
    
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

    db.insert(user)
    wiz.response.status(200,True)