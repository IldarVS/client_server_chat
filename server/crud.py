from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage_server import CClients, CHistory, CContacts
from log_run import log

engine = create_engine("sqlite:///storage_server.db")



class Crud:
    def __init__(self, ClBase):
        self.ClBase = ClBase
        # self.session = session

    @log
    def read_crud(self):
        session = sessionmaker(bind=engine)()
        # args = ClBase.username#, ClBase.information
        # print(args[0])
        crud_object = session.query(self.ClBase).all()#order_by(self.ClBase.gid.asc())
        # print("вся информация")
        # for account in crud_object:
        return crud_object

    @log
    def read_crud_id(self, id):
        session = sessionmaker(bind=engine)()
        try:
            crud_object = session.query(self.ClBase).filter_by(gid = id) #.filter_by(password=password)
            data_user = []
            for _ in crud_object:
                data_user.append(str(_))
            data_user = data_user[0]
            data_user = data_user.split(',')
            return data_user
        except Exception:
            print("неверно указан id")

    @log
    def read_crud_user(self, username):
        session = sessionmaker(bind=engine)()
        try:
            crud_object = session.query(self.ClBase).filter_by(username = username) #.filter_by(password=password)
            data_user = []
            for _ in crud_object:
                data_user.append(str(_))
            data_user = data_user[0]
            data_user = data_user.split(',')
            return data_user
        except Exception:
            pass

    @log
    def add_crud(self, *args):
        session = sessionmaker(bind=engine)()
        self.args = args
        try:
            crud_object = self.ClBase(args)
            session.add(crud_object)
            session.commit()
        except Exception:
            print('такие данные уже существуют')
            session.rollback()

    @log
    def upd_crud(self, gid, **kwargs):
        session = sessionmaker(bind=engine)()
        try:
            session.query(self.ClBase).filter(self.ClBase.gid == gid).update(kwargs)
            session.commit()

        except Exception:
            # print('произошла ошибка')
            session.rollback()

    @log
    def del_crud(self, delcrud):
        session = sessionmaker(bind=engine)()
        for crud_object in session.query(self.ClBase):
            if crud_object.gid == int(delcrud):
                session.delete(crud_object)
                session.commit()

    @log
    def print_crud(self, crud_object):
        a=[]
        for _ in crud_object:
            a.append(_)
        for _ in a:
            print(_)
if __name__ == "__main__":
    """Проверка работы с таблицей clients"""

    ClBase = CClients
    # ClBase=CHistory
    # ClBase =CContacts
    crud = Crud(ClBase)

    while True:
        cruduser = input('##############################\n'
                         'Список пользователей(r)\n'
                         '##############################\n'                   
                         'Добавить нового пользователя(a)\n' 
                         '##############################\n'
                         'Изменить пользователя(u)\n' 
                         '##############################\n'
                         'Удалить пользователя(d)\n'
                         '##############################\n' 
                         'Exit(q)\n'
                         '##############################\n')

        if cruduser =='a':
            pass
            # user = input('Имя: ')
            # password = input('пароль: ')
            # information =(input('описание: '))
            # args = (user,password,information)
            # crud.add_crud(*args)
            # crud.print_crud(crud.read_crud(*args))
        elif cruduser == 'r':
            # args=(ClBase.username ,ClBase.information)
            ClBase = CClients
            crud = Crud(ClBase)
            crud.print_crud(crud.read_crud())
            # ClBase = CHistory
            # crud.print_crud(crud.read_crud())
            # crud = Crud(ClBase)
            # ClBase = CContacts
            # crud.print_crud(crud.read_crud())
            # crud = Crud(ClBase)
        elif cruduser == 'u':

            crud.print_crud(crud.read_crud())
            upduser = input("введите № пользователя для редактирования: ")
            # passw = input("введите № пользователя для редактирования: ")
            print(crud.read_crud_id(upduser))
            if crud.read_crud_id(upduser) is None:
                print("неверно указан id")
            else:
                username = input('Введите новое имя :' )
                password = input('Измените пароль: ')
                information = input('Введите новое описание: ')
                kwargs = {'username': username, 'password': password, 'information': information}
                crud.upd_crud(upduser, **kwargs)
                crud.print_crud(crud.read_crud())
        elif cruduser == 'd':
            pass
            # print_crud(crud.read_crud())
            # deluser = input("введите № пользователя для удаления: ")
            # crud.del_crud(deluser)
            # crud.print_crud(crud.read_crud())
        elif cruduser == 'q':
            break
        else:
            print("введен неверный символ")



