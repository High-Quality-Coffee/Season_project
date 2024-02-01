import re

db = wiz.model("orm").use("user_info")


def submit():
    user=dict()
    user["id"] = wiz.request.query('id', True)
    user["name"] = wiz.request.query('name', True)
    user["email"] = wiz.request.query('email', True)
    user["password"] = wiz.request.query('password', True)

    # if not re.match(r"[^@]+@[^@]+\.[^@]+", user['email']):
    #     return wiz.response.status(401, '잘못된 이메일 형식입니다.')

    # row = userdb.get(email=user['email'])
    # if row is not None:
    #     return wiz.response.status(401, '이미 가입된 이메일입니다.')

    db.insert(user)
    wiz.response.status(200, True)
