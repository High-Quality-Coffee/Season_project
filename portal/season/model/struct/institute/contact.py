import season
import datetime
import math

class Model:
    def __init__(self, institute):
        self.institute = institute
    
    def __call__(self):
        self.institute.access()
        contactdb = self.institute.core.db("info/contact")
        userdb = self.institute.core.db("users")
        ins_id = self.institute.id
        contact = contactdb.rows(obj_type='ins', obj_id=ins_id)

        for i in range(len(contact)):
            if len(contact[i]['email']) > 0:
                uinfo = userdb.get(email=contact[i]['email'])
                if uinfo is not None:
                    contact[i]['joined'] = uinfo['created']
                else:
                    contact[i]['joined'] = False
        return contact