from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'yfarm'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)