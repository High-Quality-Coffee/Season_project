def test():
    userName=wiz.request.query("name", True)
    
    data=wiz.model('orm').use('user').get(name=userName)

    wiz.response.status(200,data)