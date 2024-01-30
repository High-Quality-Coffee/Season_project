db = wiz.model("portal/season/orm").use("user")

def login():
    id = wiz.request.query("id", True)
    password = wiz.request.query("password", True)
    user = db.get(id=id)
    if user is None:
        return wiz.response.status(401, "아이디를 확인해주세요")
    #무슨 문법인가?
    if user['password'](password) == False:
        return wiz.response.status(401, "비밀번호를 확인해주세요")
    del user['password']
    wiz.session.set(**user)
    return wiz.response.status(200, True)