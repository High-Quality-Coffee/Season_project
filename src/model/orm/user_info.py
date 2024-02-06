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
    interview=pw.CharField(max_length=32)
    duedate=pw.CharField(max_length=32)
    created=pw.CharField(max_length=11)
    #IntegerField() 는 max_length 지정해줄 필요 없음 - 지정하면 오류발생
    modified=pw.IntegerField()








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