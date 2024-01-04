import os
import season
import peewee as pw
import bcrypt
import json
import datetime

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers import algorithms, base, modes
import base64

import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

class SEED128:
    def __init__(self, iv, key):
        self.iv = bytes(iv, encoding='utf-8')
        self.key = bytes(key, encoding='utf-8')
        self.seed = algorithms.SEED(self.key)

    def encode(self, mode, text):
        cipher = base.Cipher(self.seed, mode(self.iv), backend)
        padded_text = self.pad_to_sixteen_bytes(bytes(text, 'utf-8'))
        return cipher.encryptor().update(padded_text)

    def decode(self, mode, text):
        try:
            cipher = base.Cipher(self.seed, mode(self.iv), backend)
            decoded = cipher.decryptor().update(text)
            return self.nullFlush(decoded.decode('utf-8'))
        except:
            return ""

    def nullFlush(self, text):
        result = ''
        for i in text:
            if i.encode() != b'\x00':
                result += i
        return result

    def pad_to_sixteen_bytes(self, txt):
        if len(txt) < 16:
            txt += b'\x00' * (16 - len(txt))
        return txt

seed = SEED128('Sa9zaoxz2i9szzzw', 'eCiz91Zxicjaoije')

def Model(namespace):
    class DBModel(pw.Model):
        class Meta:
            config = wiz.config("database").get(namespace)
            if config.type == 'mysql':
                opts = dict()
                for key in ['host', 'user', 'password', 'charset', 'port']:
                    if key in config:
                        opts[key] = config[key]
                database = pw.MySQLDatabase(config.database, **opts)
            else:
                sqlitedb = os.path.realpath(os.path.join(wiz.server.path.root, config.path))
                database = pw.SqliteDatabase(sqlitedb)

        class SeedField(pw.CharField):
            def db_value(self, value):
                value = [value[i:i+16] for i in range(0, len(value), 16)]
                data = ''
                for v in value:
                    encode = seed.encode(modes.CBC, v)
                    encoded64 = base64.b64encode(encode)
                    encoded64 = encoded64.decode('utf-8')
                    data += encoded64
                return data

            def python_value(self, value):
                try:
                    value = [value[i:i+24] for i in range(0, len(value), 24)]
                    data = ''
                    for v in value:
                        decoded64 = base64.b64decode(v)
                        decode = seed.decode(modes.CBC, decoded64)
                        data += decode
                    return data
                except Exception as e:
                    pass
                return ""

        class PasswordField(pw.TextField):
            def db_value(self, value):
                if value is None:
                    return value
                value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                return value

            def python_value(self, value):
                if value is None:
                    return None
                value = value.encode('utf-8')
                def check_password(password):
                    password = password.encode('utf-8')
                    return bcrypt.checkpw(password, value)
                return check_password

        class DateField(pw.DateField):
            def python_value(self, value):
                try:
                    return datetime.datetime.combine(value, datetime.datetime.min.time())
                except Exception as e:
                    pass
                return value

        class TextField(pw.TextField):
            field_type = 'LONGTEXT'

        class JSONArray(pw.TextField):
            field_type = 'LONGTEXT'

            def db_value(self, value):
                return json.dumps(value, default=str)

            def python_value(self, value):
                try:
                    if value is not None:
                        return json.loads(value)
                except Exception as e:
                    pass
                return []

        class JSONObject(pw.TextField):
            field_type = 'LONGTEXT'

            def db_value(self, value):
                return json.dumps(value, default=str)

            def python_value(self, value):
                try:
                    if value is not None:
                        return json.loads(value)
                except Exception as e:
                    pass
                return {}

        class BooleanField(pw.IntegerField):
            field_type = 'TINYINT'

            def db_value(self, value):
                if value == 'true' or value == True: return 1
                else: return 0

            def python_value(self, value):
                if value: return True
                else: return False
    
    return DBModel
