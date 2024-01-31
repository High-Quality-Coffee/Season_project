import season
import datetime
import math

class Model:
    def __init__(self, institute):
        self.institute = institute
    
    def __call__(self):
        role = self.institute.access(exception=False)
        if role == 'visitor':
            wiz.response.status(401)
        
        networkdb = self.institute.core.db("info/network")
        ins_id = self.institute.id

        if role in ['main', 'admin']:
            network = networkdb.rows(ins_id=ins_id, status='active', order="ASC", orderby="name")
        else:
            session = wiz.model("portal/season/session")
            email = session.get("email")
            contactdb = self.institute.core.db("info/contact")
            netids = contactdb.rows(fields='obj_id', obj_type='net', email=email, groupby='obj_id')
            netids = [x['obj_id'] for x in netids]
            network = networkdb.rows(ins_id=ins_id, id=netids, status='active', order="ASC", orderby="name")
        return network
