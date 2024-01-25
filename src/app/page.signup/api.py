import re

userdb = wiz.model("orm").use("user")

def submit():
    user={}
    user["id"] = wiz.request.query('id')
    user["name"] = wiz.request.query('name')
    user["email"] = wiz.request.query('email')
    user["password"] = wiz.request.query('password')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user['email']):
        return wiz.response.status(401, '잘못된 이메일 형식입니다.')

    row = userdb.get(email=user['email'])
    if row is not None:
        return wiz.response.status(401, '이미 가입된 이메일입니다.')

    userdb.insert(user)
    return wiz.response.status(200, True)
