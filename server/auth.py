from datetime import datetime
import logging
import json
from log_run import log
# import accounts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crud import Crud
from storage_server import CClients, CHistory, CContacts

code = "utf-8"
unix_time = datetime.now()


engine = create_engine("sqlite:///storage_server.db")

ClBase = CClients
# auth_crud = Crud(ClBase, session)

class Auth:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.action = kwargs['action']
        self.time = kwargs['time']
        self.user = kwargs['user']
        self.username = self.user['account_name']
        self.password = self.user['password']
    @log
    def authent(self):
        session = sessionmaker(bind=engine)()
        self.auth_pass = None
        self.auth_usr = None
        auth_user = session.query(ClBase).filter_by(username=self.username)
        for self.auth_usr in auth_user:
            print('пользователь %s в базе' % self.username)
        if self.auth_usr is None:
            cl_pres = "пользователь %s" % self.username + ' не зарегистрирован'
            msg = 'noreg'
        else:
            auth_user = session.query(ClBase).filter_by(username=self.username).filter_by(password=self.password)
            for self.auth_pass in auth_user:
                print('пользователь %s успешно авторизовался' % self.username)
            if self.auth_pass is None:
                cl_pres = "пользователь %s" % self.username + ' неверные имя пользователя или пароль'
                msg = 'exit'
            else:
                cl_pres = "пользователь %s" % self.username + ' в сети'
                msg = self.username  #
        message = json.dumps({'msg': msg, 'auth': cl_pres, 'action' :'connect'}).encode(code)

        return msg, message

    def new_reg(self):
        session = sessionmaker(bind=engine)()
        information = self.user['information']
        cl_pres = ''
        args = (self.username,self.password, information)
        try:
            new_client = ClBase(args)
            session.add(new_client)
            cl_pres = "регистрация пользователя %s" % self.username + ' завершена'
            session.commit()
        except Exception:
            cl_pres = ('такой пользователь уже сущестует')
            session.rollback()
        finally:
            print(cl_pres)
            # cl_pres = "регистрация пользователя %s" % self.username + ' завершена'
            msg = self.username
            message = json.dumps({'action': 'connect', 'msg': msg, 'auth': cl_pres}).encode(code)
        return msg, message

    @log
    def registrat(self):
        usr = Crud(ClBase)
        userid = usr.read_crud_user(self.username)
        if userid != None:
            userid=userid[0]
            usr_conn = Crud(CHistory)
            usr_conn.add_crud(userid,self.time)

    def login_required(func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            if args[1] !='':
                print(args[1])
                usr = Crud(ClBase)
                userid = usr.read_crud_user(args[1])
                if userid != None:
                    return res
        return decorated


if __name__ == "__main__":
    """ Проверка работы"""
    usr = Auth(accounts.user1)
    print(usr.authent())


