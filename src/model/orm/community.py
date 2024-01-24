import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'community'
    
    id = pw.AutoField(primary_key=True)
    user_id = pw.CharField(index=True, max_length=16)
    category = pw.CharField(index=True, max_length=16)
    title = pw.CharField(index=True, max_length=192)
    content = pw.TextField()
    files = pw.TextField()
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)