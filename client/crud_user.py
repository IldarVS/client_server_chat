from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage_client import CContactUser, CHistoryMessage

engine = create_engine("sqlite:///storage_client.db")
# session = sessionmaker(bind=engine)()


class Crud:
    def __init__(self, ClBase):
        self.ClBase = ClBase
        # self.session = session

    def read_crud(self):
        session = sessionmaker(bind=engine)()
        crud_object = session.query(self.ClBase).all()
        # print("вся информация")
        # for account in crud_object:
        data_user = []
        for _ in crud_object:
            data_user.append(str(_))
        return data_user

    def read_crud_user(self, username):
        session = sessionmaker(bind=engine)()
        try:
            crud_object = session.query(self.ClBase).filter_by(username = username) #.filter_by(password=password)
            data_user =[]
            for _ in crud_object:
                data_user.append(str(_))
            data_user = data_user[0]
            data_user = data_user.split(',')

            return data_user
        except Exception:
            pass
            # print("неверно указан id")

    def read_crud_id(self, gid):
        session = sessionmaker(bind=engine)()
        try:
            crud_object = session.query(self.ClBase).filter_by(usergid = gid) #.filter_by(password=password)
            data_user = []
            for _ in crud_object:
                data_user.append(str(_))
            data_user = data_user[0]
            data_user = data_user.split(',')
            return data_user
        except Exception:
            pass
    def add_crud(self, *args):
        session = sessionmaker(bind=engine)()
        try:
            crud_object = self.ClBase(args)
            session.add(crud_object)
            session.commit()
        except Exception:
            session.rollback()


    def upd_crud(self, gid, **kwargs):
        session = sessionmaker(bind=engine)()
        try:
            session.query(self.ClBase).filter(self.ClBase.usergid == gid).update(kwargs)
            session.commit()
        except Exception:
            print('произошла ошибка')
            session.rollback()

    def del_crud(self, delcrud):
        session = sessionmaker(bind=engine)()
        for crud_object in session.query(self.ClBase):
            if crud_object.gid == int(delcrud):
                session.delete(crud_object)
                session.commit()

    def print_crud(self, crud_object):
        for _ in crud_object:
            print(_)


if __name__ == "__main__":
    """Проверка работы с таблицей clients"""

    ClBase = CContactUser
    # ClBase =CHistoryMessage
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
            usergid = input('№: ')
            user = input('Имя: ')
            information =(input('описание: '))
            args = (usergid,user,information)
            crud.add_crud(*args)
            crud.print_crud(crud.read_crud())
        elif cruduser == 'r':
            crud.print_crud(crud.read_crud())
        elif cruduser == 'u':
            crud.print_crud(crud.read_crud())
            upduser = input("введите № пользователя для редактирования: ")
            # passw = input("введите № пользователя для редактирования: ")
            print(crud.read_crud_id(int(upduser)))
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
            print_crud(crud.read_crud())
            deluser = input("введите № пользователя для удаления: ")
            crud.del_crud(deluser)
            crud.print_crud(crud.read_crud())
        elif cruduser == 'q':
            break
        else:
            print("введен неверный символ")



