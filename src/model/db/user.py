# import peewee as pw
# base = wiz.model("orm_base")

# class Model(base):
#     class Meta:
#         db_table = 'user'

#     id = pw.CharField(max_length=32)
#     name = pw.CharField(max_length=32)
#     email = pw.CharField(unique=True, max_length=192)
#     role = pw.CharField(index=True, max_length=16, default='user')
#     password = base.PasswordField()


import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'user_info'

    id = pw.CharField(max_length=32)
    name = pw.CharField(max_length=32)
    email = pw.CharField(unique=True, max_length=192)
    role = pw.CharField(index=True, max_length=16, default='user')
    password = base.PasswordField()

