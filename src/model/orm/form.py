import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'form'

    id = pw.CharField(primary_key=True)
    first = pw.IntegerField()
    second = pw.IntegerField()
    third = pw.IntegerField()
    download = pw.IntegerField()
    title = base.TextField(unique=True)
    description = base.TextField()
    xls = pw.DateTimeField()
    ppt = pw.DateTimeField()
    hwp = pw.DateTimeField()
    doc = pw.DateTimeField()
    xlsx = pw.DateTimeField()
    pptx = pw.DateTimeField()
    hwpx = pw.DateTimeField()
    docx = pw.DateTimeField()
    pdf = pw.DateTimeField()
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)