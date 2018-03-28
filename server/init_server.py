import sqlite3

conn = sqlite3.connect('storage_server.db')
cursor = conn.cursor()

cursor.execute("""
drop table if exists clients""")
#
cursor.execute("""
drop table if exists contacts""")

cursor.execute("""
drop table if exists history_clients""")

cursor.execute("""
create table clients(
        gid integer primary key autoincrement,
        username text unique,
        password text,
        information text
        )""")

cursor.execute("""
create table history_clients(
        gid integer primary key autoincrement,
        client_gid integer references clients (gid),
        client_time text
        )""")

cursor.execute("""
 create table contacts (
        gid integer primary key autoincrement,
        owner integer references clients (gid),
        client integer references clients (gid),
        CONSTRAINT constraint_name UNIQUE (owner, client))
        """)

cursor.execute("""
insert into clients (username,password) values ('user1','pass1'), ('user2','pass2'), ('user3','pass3')

""")


cursor.execute("""insert into contacts (owner,client) values (1,1)""")
cursor.execute("""insert into contacts (owner,client) values (1,2)""")
cursor.execute("""insert into contacts (owner,client) values (1,3)""")
cursor.execute("""insert into contacts (owner,client) values (2,1)""")
cursor.execute("""insert into contacts (owner,client) values (2,2)""")
cursor.execute("""insert into contacts (owner,client) values (2,3)""")
cursor.execute("""insert into contacts (owner,client) values (3,1)""")
cursor.execute("""insert into contacts (owner,client) values (3,2)""")
cursor.execute("""insert into contacts (owner,client) values (3,3)""")
conn.commit()