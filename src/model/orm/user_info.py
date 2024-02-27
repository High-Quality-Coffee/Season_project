import peewee as pw
base=wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table='user_info'
    
    #peewee에 있는 함수들을 사용하려고 하였으나, 
    #base=wiz.model("orm_base")을 선언하여, orm_base의 함수들 사용해야 함.
    # ex) base.TextField(), base.PasswordField()

    #TextField는 LONGTEXT로 지정되어있을때만 사용해도 됨.
    #orm_base에 선언된 textfield 나 jsonarray와 같은 함수가 있을 경우 
    #orm_base에 선언된함수를 사용해야 한다.

    id=pw.IntegerField(primary_key=True)
    name=base.TextField()
    email=base.TextField()
    phone=pw.CharField(max_length=64)
    password=base.PasswordField()
    center=base.TextField()
    role=pw.CharField(max_length=11)
    interview=pw.DateTimeField()
    assignName=pw.CharField(max_length=64)
    score=pw.IntegerField()
    duedate=pw.DateTimeField()
    created=pw.CharField(max_length=11)
    #IntegerField() 는 max_length 지정해줄 필요 없음 - 지정하면 오류발생
    modified=pw.IntegerField()



