import datetime
import peewee as pw
base = wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table = 'assignment'

    id = pw.AutoField(primary_key=True)
    name=pw.CharField(max_length=11)
    email=pw.TextField()
    title=pw.TextField()
    files=pw.TextField()
    user_id=pw.IntegerField()
    notice_id=pw.IntegerField()
    due=pw.IntegerField()
    created=pw.CharField(max_length=32)
    modified=pw.CharField(max_length=32)
    role=pw.CharField(max_length=11)




# CREATE TABLE `assignment` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `name` varchar(11) DEFAULT NULL,
#   `email` longtext DEFAULT NULL,
#   `title` longtext DEFAULT NULL,
#   `files` longtext DEFAULT NULL,
#   `user_id` int(11) DEFAULT NULL,
#   `notice_id` int(11) DEFAULT NULL,
#   `due` int(11) DEFAULT NULL,
#   `created` varchar(32) DEFAULT NULL,
#   `modified` varchar(32) DEFAULT NULL,
#   `role` varchar(11) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;