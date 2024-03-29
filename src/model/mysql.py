import season
import os
import pickle
import json
import datetime
import shutil
import pymysql
import math
import string
import random
from season.util.std import stdClass

# mysql model
def join(v, format='/'):
    if len(v) == 0:
        return ''
    return format.join(v)

class Model:
    def __init__(self):
        self.wiz = wiz
        self.config = wiz.config('database')
        self.namespace = None
        self.tablename = None

    @classmethod
    def use(cls, tablename, namespace=None):
        model = cls()
        model.tablename = tablename
        model.namespace = namespace
        return model

    def __values__(self, values, **format):
        fields = self.fields()
        _field = []
        _format = []
        _update_format = []
        _data = []
        for key in values:
            if key not in fields.columns:
                continue
            _field.append('`' + key + '`')
            val = values[key]
            if val is None:
                _format.append('NULL')
                _update_format.append(f"`{key}`=NULL")
            elif key in format:
                formatstring = format[key]
                _format.append(formatstring)
                _update_format.append(f"`{key}`={formatstring}")
                if '%' in format[key]:
                    _data.append(val)
            else:
                _format.append('%s')
                _update_format.append(f"`{key}`=%s")
                _data.append(str(val))
        _field = join(_field, format=',')
        _format = join(_format, format=',')
        _update_format = join(_update_format, format=',')
        return _field, _format, _update_format, _data

    def __where__(self, where):
        IGNORE_FIELDS = ['groupby', 'orderby', 'limit', 'fields', 'where', 'like', 'or']
        fields = self.fields()
        _where = []
        _data = []

        if 'where' in where:
            scope_wheres = where['where']
            if type(scope_wheres) != list:
                scope_wheres = [scope_wheres]
            for scope_where in scope_wheres:
                if type(scope_where) == dict:
                    if 'values' in scope_where:
                        if type(scope_where['values']) != list:
                            scope_where['values'] = [scope_where['values']]
                        for v in scope_where['values']:
                            _data.append(str(v))
                    _where.append(scope_where['clause'])
                elif type(scope_where) == str:
                    _where.append(scope_where)

        if 'or' in where:
            or_where = where['or']
            _or_where = []
            _or_data = []
            for key in or_where:
                if key in IGNORE_FIELDS: continue
                if key not in fields.columns: continue
                values = or_where[key]
                if type(values) != list: values = [values]
                scope_where = []
                for value in values:
                    if type(value) != dict:
                        _v = dict()
                        _v['value'] = value
                        value = _v
                    v = value['value']
                    op = value['op'] if 'op' in value else '='
                    format = value['format'] if 'format' in value else "%s"
                    if v is None: 
                        scope_where.append(f"`{key}` {op} NULL")
                    else:
                        scope_where.append(f"`{key}` {op} {format}")
                        if '%' in format: _or_data.append(str(v))
                scope_where = "( " + join(scope_where, format=' OR ') + " )"
                _or_where.append(scope_where)

            if len(_or_where) > 0:
                _or_where = '(' + join(_or_where, format=' OR ') + ')'
                _where.append(_or_where)
                _data = _data + _or_data
        
        for key in where:
            if key in IGNORE_FIELDS: continue
            if key not in fields.columns: continue
            values = where[key]
            if type(values) != list:
                values = [values]
            scope_where = []
            for value in values:
                if type(value) != dict:
                    _v = dict()
                    _v['value'] = value
                    value = _v
                v = value['value']
                op = value['op'] if 'op' in value else '='
                format = value['format'] if 'format' in value else "%s"
                
                if v is None: 
                    scope_where.append(f"`{key}` {op} NULL")
                else:
                    scope_where.append(f"`{key}` {op} {format}")
                    if '%' in format:
                        _data.append(str(v))
            scope_where = "( " + join(scope_where, format=' OR ') + " )"
            _where.append(scope_where)
            
        if len(_where) == 0: return "", None
        _where = join(_where, format=' AND ')
        return _where, _data
            
    def query(self, sql, data=None):
        coninfo = None
        if self.namespace is not None: coninfo = self.config.data[self.namespace]
        else: coninfo = self.config.data.mysql
        con = pymysql.connect(**coninfo)
        cursor = con.cursor(pymysql.cursors.DictCursor)
        status = cursor.execute(sql, data)
        rows = cursor.fetchall()
        lastrowid = cursor.lastrowid
        con.commit()
        con.close()
        return status, rows, lastrowid

    def fields(self):
        tablename = self.tablename
        _, columns, _ = self.query('DESC ' + tablename)
        result = stdClass()
        result.pk = []
        result.columns = []
        for col in columns:
            if col['Key'] == 'PRI':
                result.pk.append(col['Field'])
            result.columns.append(col['Field'])
        return result

    def insert(self, values, **format):
        try:
            tablename = self.tablename
            _field, _format, _, _data = self.__values__(values, **format)
            sql = f"INSERT INTO `{tablename}`({_field}) VALUES({_format})"
            _, _, lastrowid = self.query(sql, data=_data)
            return True, lastrowid
        except Exception as e:
            return False, e

    def upsert(self, values, **format):
        try:
            tablename = self.tablename
            _field, _format, _update_format, _data = self.__values__(values, **format)
            _data = _data + _data
            sql = f"INSERT INTO `{tablename}`({_field}) VALUES({_format}) ON DUPLICATE KEY UPDATE {_update_format}"
            status, _, lastrowid = self.query(sql, data=_data)
            if status == 0:
                return True, -1
            return True, lastrowid
        except Exception as e:
            print(e)
            return False, e

    def get(self, **where):
        try:
            tablename = self.tablename
            orderby = None
            if 'orderby' in where:
                orderby = where['orderby']
                del where['orderby']
            groupby = None
            if 'groupby' in where:
                groupby = where['groupby']
                del where['groupby']
            limit = None
            if 'limit' in where:
                limit = where['limit']
                del where['limit']
            
            targetfields = '*'
            if 'fields' in where:
                targetfields = where['fields']
            wherestr, wheredata = self.__where__(where)
            sql = f"SELECT {targetfields} FROM `{tablename}` WHERE {wherestr}"

            if groupby is not None:
                sql = sql + ' GROUP BY ' + groupby
            if orderby is not None:
                sql = sql + ' ORDER BY ' + orderby
            if limit is not None:
                sql = sql + ' LIMIT ' + str(limit)

            _, rows, _ = self.query(sql, wheredata)
            if len(rows) > 0:
                return rows[0]
            return None
        except Exception as e:
            return None

    def count(self, **where):
        try:
            orderby = None
            if 'orderby' in where:
                orderby = where['orderby']
                del where['orderby']
            groupby = None
            if 'groupby' in where:
                groupby = where['groupby']
                del where['groupby']

            tablename = self.tablename
            wherestr, wheredata = self.__where__(where)
            if len(wherestr) > 0:
                sql = 'SELECT count(*) AS cnt FROM `' + tablename + '` WHERE ' + wherestr
            else:
                sql = 'SELECT count(*) AS cnt FROM `' + tablename + '`'

            if groupby is not None:
                sql = sql + ' GROUP BY ' + groupby
            if orderby is not None:
                sql = sql + ' ORDER BY ' + orderby

            _, rows, _ = self.query(sql, wheredata)

            return rows[0]['cnt']
        except Exception as e:
            return 0

    def count_c(self, **where):
        try:
            orderby = None
            if 'orderby' in where:
                orderby = where['orderby']
                del where['orderby']
            groupby = None
            if 'groupby' in where:
                groupby = where['groupby']
                del where['groupby']

            tablename = self.tablename
            wherestr, wheredata = self.__where__(where)

            if len(wherestr) > 0:
                sql = 'SELECT count(*) AS cnt FROM `' + tablename + '` WHERE ' + wherestr
            else:
                sql = 'SELECT count(*) AS cnt FROM `' + tablename + '`'

            if groupby is not None:
                # sql = sql + ' GROUP BY ' + groupby
                sql = 'SELECT ' + groupby + ' AS name, count(*) AS cnt FROM `' + tablename + '` GROUP BY ' + groupby
            if orderby is not None:
                sql = sql + ' ORDER BY ' + orderby

            _, rows, _ = self.query(sql, wheredata)

            return rows
        except Exception as e:
            return 0
    
    def select(self, **where):
        return self.rows(**where)

    def rows(self, **where):
        try:
            tablename = self.tablename
            orderby = None
            if 'orderby' in where:
                orderby = where['orderby']
                del where['orderby']
            groupby = None
            if 'groupby' in where:
                groupby = where['groupby']
                del where['groupby']
            limit = None
            if 'limit' in where:
                limit = where['limit']
                del where['limit']

            targetfields = '*'
            if 'fields' in where:
                targetfields = where['fields']
            wherestr, wheredata = self.__where__(where)
            if len(wherestr) > 0:
                sql = f'SELECT {targetfields} FROM `{tablename}` WHERE {wherestr}'
            else:
                sql = f'SELECT {targetfields} FROM `{tablename}`'

            if groupby is not None:
                sql = sql + ' GROUP BY ' + groupby
            if orderby is not None:
                sql = sql + ' ORDER BY ' + orderby
            if limit is not None:
                sql = sql + ' LIMIT ' + str(limit)
            _, rows, _ = self.query(sql, data=wheredata)
            return rows
        except Exception as e:
            print(e)
            return []

    def delete(self, **where):
        try:
            tablename = self.tablename
            wherestr, wheredata = self.__where__(where)
            if len(wherestr) > 0:
                sql = 'DELETE FROM `' + tablename + '` WHERE ' + wherestr
            else:
                sql = 'DELETE FROM `' + tablename + '`'
            _, _, _ = self.query(sql, wheredata)
            return True
        except Exception as e:
            return False

    def update(self, values, **where):
        try:
            tablename = self.tablename
            _, _, _update_format, _data = self.__values__(values)
            wherestr, wheredata = self.__where__(where)
            sql = f"UPDATE `{tablename}` SET {_update_format} WHERE {wherestr}"
            _data = _data + wheredata
            res, _, _ = self.query(sql, data=_data)
            if res == 0: return True, "Nothing Changed"
            return True, "Success"
        except Exception as e:
            print(e)
            return False, e

    def search(self, **query):
        IGNORED_FIELDS = ['page', 'size', 'like']
        page = int(query['page']) if 'page' in query else 1
        size = int(query['size']) if 'size' in query else 20 
        likes = query['like'] if 'like' in query else []
        if type(likes) == str: likes = likes.split(',')
        for like in likes:
            if like in query:
                if type(query[like]) == dict: 
                    continue
                query[like] = {"value": "%" + str(query[like]) + "%", "op": "LIKE"}
            if 'or' in query:
                if like in query['or']:
                    if type(query['or'][like]) == dict: 
                        continue
                    query['or'][like] = {"value": "%" + str(query['or'][like]) + "%", "op": "LIKE"}
        for f in IGNORED_FIELDS:
            if f in query: del query[f]
        page = (page - 1) * size
        query['limit'] = f"{page}, {size}"
        result = dict()

        rows = self.select(**query)
        result['list'] = rows

        del query['limit']
        if 'orderby' in query: del query['orderby']
        if 'fields' in query: del query['fields']
        query['fields'] = "count(*) AS cnt"
        
        totalcount = self.rows(**query)

        if len(totalcount) > 1:
            totalcount = len(totalcount)
        else:
            totalcount = totalcount[0]['cnt']
        result['lastpage'] = math.ceil(totalcount / size)
        result['page'] = page + 1
        result['size'] = size

        return result

    def search_facet(self, **query):
        IGNORED_FIELDS = ['page', 'size', 'like']
        page = int(query['page']) if 'page' in query else 1
        size = int(query['size']) if 'size' in query else 20 
        likes = query['like'] if 'like' in query else []
        if type(likes) == str: likes = likes.split(',')
        for like in likes:
            if like in query:
                if type(query[like]) == dict: 
                    continue
                query[like] = {"value": "%" + str(query[like]) + "%", "op": "LIKE"}
            if 'or' in query:
                if like in query['or']:
                    if type(query['or'][like]) == dict: 
                        continue
                    query['or'][like] = {"value": "%" + str(query['or'][like]) + "%", "op": "LIKE"}
        for f in IGNORED_FIELDS:
            if f in query: del query[f]
        page = (page - 1) * size
        query['limit'] = f"{page}, {size}"
        result = dict()

        rows = self.select(**query)
        result['list'] = rows

        del query['limit']
        if 'orderby' in query: del query['orderby']
        if 'fields' in query: del query['fields']
        query['fields'] = "count(*) AS cnt"
        
        totalcount = self.rows(**query)

        if len(totalcount) > 1:
            totalcount = len(totalcount)
        else:
            totalcount = totalcount[0]['cnt']
        result['lastpage'] = math.ceil(totalcount / size)
        result['page'] = page + 1
        result['size'] = size
        
        # dataset facet 추가 (검색필터)
        result['total'] = totalcount

        result['facet'] = dict()
        
        query['orderby'] = 'cnt DESC'

        query['fields'] = 'department AS name, count(*) AS cnt'
        query['groupby'] = 'department'
        result['facet']['department'] = self.rows(**query)
        
        query['fields'] = 'category AS name, count(*) AS cnt'
        query['groupby'] = 'category'
        result['facet']['category'] = self.rows(**query)

        query['fields'] = 'datatype AS name, count(*) AS cnt'
        query['groupby'] = 'datatype'
        result['facet']['datatype'] = self.rows(**query)

        query['fields'] = 'visibility AS name, count(*) AS cnt'
        query['groupby'] = 'visibility'
        result['facet']['visibility'] = self.rows(**query)

        # if 
        return result

    def login(self, email, password):
        _, session_info, _ = self.query('SELECT * FROM users WHERE email=%s AND password=password(%s)', data=[email, password])
        if len(session_info) == 0:
            return None
        session_info = session_info[0]
        del session_info['password']
        return session_info

    def up(self, dataset_id):
        try:
            data = dict()
            data['user_id'] = self.wiz.session.get('id')
            data['dataset_id'] = dataset_id
            stat, _ = self.insert(data)
            if stat == False:
                self.delete(user_id=data['user_id'], dataset_id=data['dataset_id'])
            return True
        except:
            return False

    # view.explore.view.item -> dataset_shared
    def open(self, dataset_id, user_id):
        obj = Model(self.framework)
        obj.dataset_id = dataset_id
        obj.user_id = user_id
        return obj

    # 조회수 업데이트 (log_access)
    def upsert_log(self, namespace, timecheck=0):
        try:
            # 랜덤 코드 생성
            string_pool = string.ascii_letters + string.digits
            result = ""
            for i in range(18):
                result += random.choice(string_pool)

            if not wiz.session.get('SF_SESSION_ID'):
                sid = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + result
                # wiz.session.set('SF_SESSION_ID', sid)
            else:
                sid = wiz.session.get('SF_SESSION_ID')

            if timecheck > 0:
                cnt = self.count(session_id=sid, namespace=namespace, where=f"`accesstime` >= DATE_SUB(now(), INTERVAL {timecheck} HOUR)")
                if cnt > 0: return False, "CHECKED"

            values = dict()
            values['namespace'] = namespace
            values['session_id'] = sid
            values['user_id'] = "undefined"
            values['useragent'] = wiz.request.request().user_agent.string
            values['access_ip'] = wiz.request.client_ip()
            values['full_url'] = wiz.request.uri()

            if wiz.session.get('id'): values['user_id'] = wiz.session.get('id')
           
            status, lastrowid = self.upsert(values)
            return status, lastrowid
        except Exception as e:
            return False, e