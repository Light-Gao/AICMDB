"""Author  Light Gao
Mailto  gaoliang@asiainfo.com
Date    20180112
Last Modified 20180228"""
from flask_sqlalchemy import SQLAlchemy
from apm.extensions import bcrypt
from apm.enums import globalenums

#Generate db object without app object,
#which should be initialed in apm.__init__()
db = SQLAlchemy()

#Model for table "apm_user", manual table structure
class User(db.Model):
    __tablename__ = 'apm_user'
    apm_user_id = db.Column(db.Integer, primary_key=True)
    apm_user_name = db.Column(db.String(64))
    apm_user_passwd = db.Column(db.String(255))
    status = db.Column(db.String(16))
    remark = db.Column(db.String(255))
    #one to many virtual columns
    service = db.relationship('Service', backref='apm_user', lazy='dynamic')
    resource = db.relationship('Resource', backref='apm_user', lazy='dynamic')
    svc_instance = db.relationship('SvcInstance', backref='apm_user', lazy='dynamic')

    #init function
    def __init__(self, user_name=None, user_passwd=None):
        self.apm_user_name = user_name
        self.apm_user_passwd = self.set_passwd(user_passwd)
        self.status = globalenums.DEFAULT_STATUS_VALUE
        self.remark = None

    #define the style when execute print(user_object)
    def __repr__(self):
        output = "(%s,%s,%s,%s,%s)" % \
                 (self.apm_user_id, self.apm_user_name,
                  self.apm_user_passwd, self.status, self.remark)
        return output

    @staticmethod
    def set_passwd(passwd):
        return bcrypt.generate_password_hash(passwd)

    #take plain-text passwd as input
    def check_passwd(self, passwd):
        return bcrypt.check_password_hash(self.apm_user_passwd, passwd)

#Table for relationship between service and resource
#Must defined before class Service in case could not resolve svc_res
#We cannot operator this table directly, so we use Table instead of Model
svc_res = db.Table('apm_svc_res_rel',
                   db.Column('apm_svc_res_rel_id', db.Integer, primary_key=True),
                   db.Column('apm_service_id', db.Integer, db.ForeignKey('apm_service.apm_service_id')),
                   db.Column('apm_resource_id', db.Integer, db.ForeignKey('apm_resource.apm_resource_id')))

'''Model for table apm_service'''
class Service(db.Model):
    __tablename__ = 'apm_service'
    apm_service_id = db.Column(db.Integer, primary_key=True)
    apm_service_name = db.Column(db.String(128))
    status = db.Column(db.String(8))
    create_date = db.Column(db.DateTime)
    apm_user_id = db.Column(db.Integer, db.ForeignKey('apm_user.apm_user_id'))
    remark = db.Column(db.String(255))
    #one to many virtual columns
    svc_instance = db.relationship('SvcInstance', backref='apm_service', lazy='dynamic')
    #many to many virtual columns
    resource = db.relationship('Resource', secondary=svc_res,
                               backref=db.backref('apm_service', lazy='dynamic'))

    def __repr__(self):
        output = "(%s,%s,%s,%s)" % \
                 (self.apm_service_id, self.apm_service_name,
                  self.status, self.apm_user_id)
        return output

'''Model for table apm_resource'''
class Resource(db.Model):
    __tablename__ = 'apm_resource'
    apm_resource_id = db.Column(db.Integer, primary_key=True)
    apm_resource_name = db.Column(db.String(128))
    status = db.Column(db.String(8))
    apm_user_id = db.Column(db.Integer, db.ForeignKey('apm_user.apm_user_id'))
    create_date = db.Column(db.DateTime)
    remark = db.Column(db.String(255))

    def __repr__(self):
        output = "(%s,%s,%s,%s)" % \
                 (self.apm_resource_id, self.apm_resource_name,
                  self.status, self.apm_user_id)
        return output

'''Model for table apm_svc_instance'''
class SvcInstance(db.Model):
    __tablename__ = 'apm_svc_instance'
    apm_svc_inst_id = db.Column(db.Integer, primary_key=True)
    apm_svc_inst_name = db.Column(db.String(128))
    apm_service_id = db.Column(db.Integer, db.ForeignKey('apm_service.apm_service_id'))
    status = db.Column(db.String(8))
    create_date = db.Column(db.DateTime)
    apm_user_id = db.Column(db.Integer, db.ForeignKey('apm_user.apm_user_id'))
    remark = db.Column(db.String(255))

    def __repr__(self):
        output = "(%s,%s,%s,%s,%s,%s)" % \
                 (self.apm_svc_inst_id, self.apm_svc_inst_name,
                  self.apm_service_id, self.status, self.create_date,
                  self.apm_user_id)
        return output
