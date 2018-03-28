from sqlalchemy import Table, Column, Integer, UniqueConstraint, ForeignKey, Unicode, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


CBase = declarative_base()

class CContactUser(CBase):
    __tablename__ = "contacts"
    gid = Column(Integer(), primary_key=True)
    usergid = Column(Integer())
    username = Column(Unicode())
    information = Column(Unicode())
    check_1 = UniqueConstraint("usergid")

    def __init__(self, *args, **kwargs):
        self.args = args[0]
        self.kwargs = kwargs
        self.usergid = self.args[0]
        self.username = self.args[1]
        self.information = self.args[2]

    def __repr__(self):
        return "%d,%s,%s" % (self.usergid, self.username, self.information)

class CHistoryMessage(CBase):
    __tablename__ = "history_messages"
    gid = Column(Integer(), primary_key = True)
    client_from = Column(Integer(), ForeignKey("contacts.gid"))
    client_to = Column(Integer(), ForeignKey("contacts.gid"))
    message = Column(Unicode())
    message_time = Column(Unicode())

    def __init__(self, *args, **kwargs):
        self.args = args[0]
        self.kwargs = kwargs
        self.client_from = self.args[0]
        self.client_to = self.args[1]
        self.message = self.args[2]
        self.message_time = self.args[3]


    def __repr__(self):
        return "%d,%d,%s,%s" % (self.client_from, self.client_to, self.message, self.message_time)



#######################################################################################################
if __name__ == "__main__":
    """
     Проверка работы
     """

    engine = create_engine("sqlite:///storage_client.db")
    session = sessionmaker(bind = engine)()
    #
    users = session.query(CContactUser).all()
    #
    for user in users:
        print(user)

