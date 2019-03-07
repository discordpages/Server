import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini')

class DataBase:
  """
  DataBase class that handles all PostgreSQL queries

  Attributes
  ----------
  con : Connection
    a connection to the database
  cur : Cursor
    the database cursor to execute queries

  Methods
  -------
  create_table()
    Creates the default servers channel
  """

  def __init__(self):
    """Initialize class variables"""
    self.con = None
    self.cur = None

  def connect(self, host, username, password):
    """Connects to the database.

    Connect to the postgresql server and assign con and cur.

    Parameters
    ----------
    username : str
      Authentication username
    host : str
      Database host URL
    password: str
      Authentication password

    Returns
    -------
    Boolean
      Whether connection succeeds or not
    """
    try:
      sys.stdout.write("Connecting to local database... ")
      self.con = psycopg2.connect(dbname='postgres',
        user=username,
        host=host,
        password=password)
      self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
      self.cur = self.con.cursor()
      sys.stdout.write("CONNECTED.\r\n")
      return True
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
      return False


  def create_table(self):
    """Create server table.

    Checks if the table exists first before creating the table that stores the
    servers.

    Returns
    -------
    Boolean
      Whether table exists
    """
    sys.stdout.write("Checking table exists... ")
    self.cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='servers');")

    if self.cur.fetchone() == None:
      sys.stdout.write("TABLE DOES NOT EXIST.\r\nCreating new table... ")
      try:
        self.cur.execute("CREATE TABLE servers ( \
          server_id serial PRIMARY KEY, \
          server_name TEXT NOT NULL, \
          server_description TEXT, \
          server_invite VARCHAR (40) NOT NULL, \
          server_added_date TIMESTAMP NOT NULL \
        );")
        sys.stdout.write("TABLE CREATED.\r\n")
        return True
      except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

    sys.stdout.write("TABLE EXISTS.\r\n")
    return True
  
  def add_server(self, server_name, server_invite, server_description=None):
    """Adds a server to the database.

    Parameters
    ----------
    server_name : str
      Name of the server
    server_invite : str
      Server invite link
    server_description: str, optional
      Optional server description

    Returns
    -------
    Boolean
      If the insertion succeeded
    """
    now = datetime.now()
    sys.stdout.write("Adding server... ")
    try:
      self.cur.execute("INSERT INTO servers \
        (server_name, server_description, server_invite, server_added_date) \
        VALUES (%s, %s, %s, %s)",
        (server_name, server_description, server_invite, now))
      sys.stdout.write("ADDED.")
      return True
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
      return False

  def close_connection(self):
    """Cleanup.
    
    Closes database cursor and then connection.
    """
    self.cur.close()
    self.con.close()


db = DataBase()
db.connect(config['DEFAULT']['host'], config['DEFAULT']['username'], config['DEFAULT']['password'])
db.create_table()
db.close_connection()