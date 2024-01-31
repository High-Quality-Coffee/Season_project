import season
import datetime
import math

orm = wiz.model("portal/season/orm")
Contact = wiz.model("portal/kreonet/struct/institute/contact")
Network = wiz.model("portal/kreonet/struct/institute/network")

class Model:
    def __init__(self, core):
        self.namespace = None
        self.id = None
        self.core = core
    
    def __call__(self, _namespace):
        mod = Model(self.core)
        mod.namespace = _namespace
        data = mod.data()
        mod.id = data['id']
        mod.contact = Contact(mod)
        mod.network = Network(mod)
        return mod

    def search(self, page=1, dump=30, orderby="id", order="ASC", **where):
        db = self.core.db("info/institute")

        session = wiz.model("portal/season/session")
        if session.get("role") != 'admin' or self.core.isAdmin is False:
            contactdb = self.core.db("info/contact")
            email = session.get("email")
            
            nets = contactdb.rows(fields="obj_id", obj_type='net', email=email, groupby="obj_id")
            nets = [x['obj_id'] for x in nets]

            fromnet = []
            if len(nets) > 0:
                networkdb = self.core.db("info/network")
                insids = networkdb.rows(fields="ins_id", id=nets, groupby="ins_id")
                insids = [x['ins_id'] for x in insids]
                fromnet = insids

            insids = contactdb.rows(fields='obj_id', obj_type='ins', email=email, groupby='obj_id')
            insids = [x['obj_id'] for x in insids]

            where['id'] = insids + fromnet

            if len(where['id']) == 0:
                return [], 0
        
        rows = db.rows(page=page, dump=dump, orderby="id", order="ASC", **where)
        total = db.count(**where)
        return rows, total
    
    def role(self, email):
        if self.id is None: return None, []
        contactdb = self.core.db("info/contact")
        mainrole = contactdb.get(fields="role", obj_type='ins', obj_id=self.id, email=email)
        if mainrole is not None: mainrole = mainrole['role']
        
        networkdb = self.core.db("info/network")
        nets = networkdb.rows(fields="id", status="active", ins_id=self.id)
        nets = [x['id'] for x in nets]

        netrole = contactdb.rows(fields="role", obj_type='net', obj_id=nets, email=email)
        netrole = [x['role'] for x in netrole]
        return mainrole, netrole

    def access(self, role=['admin', 'main', 'sub'], exception=True):
        def getRole():
            session = wiz.model("portal/season/session")
            if self.core.isAdmin:
                if session.get("role") == 'admin':
                    return 'admin'
            email = session.get("email")
            main, sub = self.role(email)
            if main is not None:
                return 'main'
            if len(sub) > 0:
                return 'sub'
            return 'visitor'
        target = getRole()
        if exception and target not in role:
            wiz.response.status(401)
        return target

    def data(self):
        if self.namespace is None: return None
        db = self.core.db("info/institute")
        data = db.get(namespace=self.namespace)
        self.id = data['id']
        self.access()
        return data

    def update(self, data):
        if self.namespace is None: return False
        self.access()
        db = self.core.db("info/institute")
        if 'id' in data: del data['id']
        if 'namespace' in data: del data['namespace']
        db.update(data, id=self.namespace)
        return True
