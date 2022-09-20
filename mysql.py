import pymysql
from conf import conf

mysql_conf = conf['mysql_conf']
conn = pymysql.connect(host=mysql_conf['host'], user=mysql_conf['user'], password=mysql_conf['password'], database=mysql_conf['db'], charset=mysql_conf['charset'])
cur = conn.cursor()