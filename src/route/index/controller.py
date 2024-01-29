# wiz.model('orm').use('comment').create()
wiz.model('orm').use('community').create()
# wiz.model('orm').use('form').create()
wiz.response.redirect("/community/list;category=notice")