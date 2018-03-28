from sqlalchemy import Table, Column, Integer, UniqueConstraint, ForeignKey, Unicode, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from log_run import log

CBase = declarative_base()
class CClients(CBase):
    __tablename__ = "clients"
    gid = Column(Integer(), primary_key = True)
    username = Column(Unicode())
    password = Column(Unicode())
    information = Column(Unicode())
    check_1 = UniqueConstraint("username")

    def __init__(self, *args,**kwargs):
        self.args = args[0]
        self.kwargs = kwargs
        self.username = self.args[0]
        self.password = self.args[1]
        self.information = self.args[2]

    @log
    def __repr__(self):
        return "%d,%s,%s" % (self.gid, self.username, self.information)

class CHistory(CBase):
    __tablename__ = "history_clients"
    gid = Column(Integer(), primary_key = True)
    client_gid = Column(Integer(), ForeignKey("clients.gid"))
    client_time =Column(Unicode())

    def __init__(self, *args):
        self.args = args[0]
        self.client_gid = self.args[0]
        self.client_time = self.args[1]

    @log
    def __repr__(self):
        return "CHistory<gid = %d, client_gid =%d, client_time =%s>" % (self.gid, self.client_gid, self.client_time)


class CContacts(CBase):
    __tablename__ = "contacts"
    gid = Column(Integer(), primary_key=True)
    owner = Column(Integer(), ForeignKey("clients.gid"))
    client = Column(Integer(), ForeignKey("clients.gid"))
    check_2 = UniqueConstraint("owner", 'client')

    p_owner = relationship("CClients", foreign_keys=[owner])
    p_client = relationship("CClients", foreign_keys = [client])

    def __init__(self, *args):
        self.args = args[0]
        self.owner = self.args[0]
        self.client = self.args[1]

    @log
    def __repr__(self):
        return "CContacts<gid = %d, owner =%d, client = %d>" % (self.gid, self.owner, self.client)


#######################################################################################################
if __name__ == "__main__":
    """
     Проверка работы
     """

    engine = create_engine("sqlite:///storage_server.db")
    session = sessionmaker(bind = engine)()
    #
    users = session.query(CClients).all()
    #
    for user in users:
        print(user)

    contacts = session.query(CContacts).all() #.filter_by(gid = 1)

    for contact in contacts:
        print(contact.p_owner, contact.p_client)