DEBUG = True


#connect database
#dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'thankyou'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'account'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST
                                ,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False



