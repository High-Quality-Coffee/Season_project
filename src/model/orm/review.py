import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'review'
    
    id=pw.AutoField(primary_key=True)
    name=pw.CharField(max_length=32)
    email=pw.CharField(max_length=64)
    user_id=pw.IntegerField()
    assignment_id=pw.IntegerField()
    content=pw.TextField()
    score=pw.IntegerField()
    created=pw.CharField(max_length=11)
    modified=pw.CharField(max_length=11)