class Config:
    SECRET_KEY = 'dp1HksP7$'

class DevelopmentConfig(Config):
	DEBUG = True
	MYSQL_HOST = 'localhost'
	MYSQL_USER = 'root'
	MYSQL_PASSWORD = 'Ax98kc11$'
	MYSQL_DB = 'flaskdb'

config = {
	'development': DevelopmentConfig
}
