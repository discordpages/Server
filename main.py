import importlib
import configparser

importlib.import_module('database.py')
importlib.import_module('server.py')

config = configparser.ConfigParser()
config.read('config.ini')

db = DataBase()
db.connect(config['DEFAULT']['host'], config['DEFAULT']['username'], config['DEFAULT']['password'])
db.create_table()
db.close()