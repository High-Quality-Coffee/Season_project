import season
import time
import datetime
import os
import urllib

orm = wiz.model("orm")

segment = wiz.request.match("/file/<action>/<category>/<file_id>/<path:path>")
action = segment.action
category = segment.category
file_id = segment.file_id

fs = season.util.os.FileSystem(os.path.join(wiz.config("config").STORAGE_PATH, f"{category}/{file_id}"))
user_id = wiz.session.get("id", None)

if action == 'upload':
    file = wiz.request.file("upload")    
    if len(file.filename) == 0: 
        wiz.response.status(404)

    filepath = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + orm.random(8)
    fs.write.file(filepath, file)
    urlfilename = urllib.parse.quote(file.filename)
    wiz.response.json({"url": f'/file/download/{category}/{file_id}/{filepath}/{urlfilename}'})

elif action == 'download':
    segment = wiz.request.match("/file/<action>/<category>/<file_id>/<filepath>/<filename>")
    attatch = wiz.request.query("attatch", None)
    filepath = segment.filepath
    filepath = urllib.parse.unquote(filepath)
    filename = segment.filename
    filename = urllib.parse.unquote(filename)
    # if fs.isfile(filepath) == False:
    #     wiz.response.abort(404)
        
    filepath = fs.abspath(filepath)
    wiz.response.download(filepath, as_attachment=attatch, filename=filename)


elif action == 'delete':
    filepath = os.path.join(categoty, filename)
    if fs.isfile(filepath) == False:
        wiz.response.abort(404)

    fs.remove(filepath)

    wiz.response.status(200)
