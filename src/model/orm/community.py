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
    created = pw.CharField(index=True,max_length=32)
    updated = pw.CharField(index=True,max_length=16)


#     CREATE TABLE `community` (
#   `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `user_id` varchar(16) DEFAULT NULL,
#   `category` varchar(16) DEFAULT NULL,
#   `title` varchar(192) DEFAULT NULL,
#   `content` longtext DEFAULT NULL,
#   `files` longtext DEFAULT NULL,
#   `created` datetime DEFAULT NULL,
#   `updated` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;