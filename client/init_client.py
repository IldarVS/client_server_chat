import sqlite3

conn = sqlite3.connect('storage_client.db')
cursor = conn.cursor()

cursor.execute("""
drop table if exists contacts""")

cursor.execute("""
drop table if exists history_messages""")

cursor.execute("""
 create table contacts(
        gid integer primary key autoincrement,
        usergid integer unique,
        username text,
        information text
           )""")

cursor.execute("""
create table history_messages(
        gid integer primary key autoincrement,
        client_from integer references contacts (gid),
        client_to integer references contacts (gid),
        message text,
        message_time text
        )""")

conn.commit()