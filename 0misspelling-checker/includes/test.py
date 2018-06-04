__author__ = 'electop.yoo@samsung.com'

import sys
import mysql.connector
from mysql.connector import errorcode

user = 'user'
password = ''
host = ''
database = ''
config = {}

args = sys.argv[0:]
optionLen = len(args)

def init():

  global user, password, host, database, config

  if (len(args) <= 1):
    print('[ERR] There is no option')
    return False

  for i in range(optionLen-1):
    data = str(args[i+1])
    if args[i].upper() == '-U':		# -U : user name of MySQL (e.g.: root)
      user = data
    elif args[i].upper() == '-P':	# -P : password of username
      password = data
    elif args[i].upper() == '-H':	# -H : host of MySQL (e.g.: 127.0.0.1)
      host = data
    elif args[i].upper() == '-D':	# -D : database name (e.g.: wp_aitest)
      database = data

  if (user == '') or (password == '') or (host == '') or (database == ''):
    print('[ERR] Please input all required data like user, password, host and database name.')
    return False
  else:
    config = {
    'user': user,
    'password': password,
    'host': host,
    'database': database,
    'raise_on_warnings': True,
    }
  return True

if init():
  try:
    cnx = mysql.connector.connect(**config)
    print('[OK] Connection success')
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print('[ERR] Something is wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print('[ERR] Database does not exist')
    else:
      print('[ERR]', err)
  else:
    cnx.close()
else:
  print("[ERR] Connection failure")
