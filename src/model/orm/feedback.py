import re
import datetime
import peewee as pw

base=wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table='feedback'

    id=pw.AutoField(primary_key=True)
    user_email=pw.CharField(max_length=64)
    user_name=pw.CharField(max_length=32)
    title=pw.CharField(max_length=64)
    content=pw.TextField()
    writer=pw.CharField(max_length=11)
    created=pw.DateTimeField()
    updated=pw.DateTimeField()