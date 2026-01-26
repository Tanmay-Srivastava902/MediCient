from service_managers import mysql_services
from core_app import users
import errors
conn = mysql_services.create_conn(password='SecurePass@1201',db='medicient')
cursor = conn.cursor()
try:
    # users.register(cursor)
    demo_passphrase = "tsri@hello.passhrase"
    users.register(cursor,demo_passphrase)
    # if users.login(cursor):
    #     print("user logged in")
    conn.commit()
    conn.close()
except errors.DBError as e :
    print(e)
    conn.close()