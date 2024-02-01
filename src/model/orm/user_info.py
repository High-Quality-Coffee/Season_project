import peewee as pw
base=wiz.model("orm_base")

class Model(base):
    class Meta:
        db_table='user_info'

    id=pw.IntegerField(primary_key=True)
    name=pw.TextField()
    email=pw.TextField()
    phone=pw.CharField(max_length=64)
    password=pw.TextField()
    center=pw.TextField()
    role=pw.TextField()
    interview=pw.CharField(max_length=32)
    created=pw.CharField(max_length=11)
    modified=pw.IntegerField(max_length=11)









# CREATE TABLE `user_info` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `name` text DEFAULT NULL,
#   `email` text DEFAULT NULL,
#   `phone` varchar(64) DEFAULT NULL,
#   `password` text DEFAULT NULL,
#   `center` text DEFAULT NULL,
#   `role` text DEFAULT NULL,
#   `interview` varchar(32) DEFAULT NULL,
#   `created` varchar(11) DEFAULT NULL,
#   `modified` int(11) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;