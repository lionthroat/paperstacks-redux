from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'cxeqsk4416lwhuri'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ch4at87dhgpuv005'
app.config['MYSQL_DATABASE_DB'] = 'e17gpbo1zl8mbfi9'
app.config['MYSQL_DATABASE_HOST'] = 'spvunyfm598dw67v.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql.init_app(app)
