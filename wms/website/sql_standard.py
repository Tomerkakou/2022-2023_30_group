import sqlalchemy
import datetime


def query(querey):
    try:
        user = 'db_user'
        password = 'db_user_pass'
        host = 'localhost'
        port = 3306
        database = 'app_db'
        db=sqlalchemy.create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            )
        )
        result = db.execute(querey).fetchall()
        if len(result[0])==0:
            raise ValueError
    except:
        return None

def update(str):
    try:
        user = 'db_user'
        password = 'db_user_pass'
        host = 'localhost'
        port = 3306
        database = 'app_db'
        db=sqlalchemy.create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            )
        )
        db.execute(str)
        return True
    except:
        return None




    
    
    
    

 


