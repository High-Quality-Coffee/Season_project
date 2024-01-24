import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'comment'
    
    id = pw.AutoField(primary_key=True)
    community_id = pw.IntegerField(index=True)
    user_id = pw.CharField(index=True, max_length=16)
    content = pw.TextField()
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)