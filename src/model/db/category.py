import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'category'

    id = pw.AutoField(primary_key=True)
    pid = pw.IntegerField()
    depth = pw.IntegerField()
    name = pw.CharField(index=True, max_length=16)
