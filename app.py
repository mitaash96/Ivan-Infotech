from flask import *
from flaskext.mysql import MySQL
import pandas as pd

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'mitaash'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Pmitaash_2607'
app.config['MYSQL_DATABASE_DB'] = 'sql_invoicing'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor =conn.cursor()

@app.route('/')
def default1():
   dictmanual = {"Default":"http://127.0.0.1:5000/",
   "By_IFSC":"http://127.0.0.1:5000/bank_ifsc/<ifsc>/<offset>/<limit>",
   "By_BANKNAME_CITY":"http://127.0.0.1:5000/bank_name_city/<bname>/<bcity>/<offset>/<limit>",}

   return jsonify(dictmanual)

@app.route('/bank_ifsc/<ifsc>/<int:offset>/<int:limit>', methods = ["GET"])
def func1(ifsc,offset,limit):

   if offset>0: offset = 0
   
   sql_query = """ SELECT * FROM branches WHERE ifsc = %s LIMIT %s , %s """
   cursor.execute(sql_query, (ifsc,offset,limit))
   records = cursor.fetchall()
   df = pd.DataFrame(records)
   df.columns = ['IFSC','BANK_ID','BRANCH','ADDRESS','CITY','DISTRICT','STATE','BANK_NAME']

   return jsonify(df.to_dict(orient= 'records'))

@app.route('/bank_name_city/<bname>/<bcity>/<int:offset>/<int:limit>', methods = ["GET"])
def func2(bname, bcity,offset,limit):
   
   sql_query = """ SELECT * FROM branches WHERE bank_name = %s AND city = %s LIMIT %s , %s """
   cursor.execute(sql_query, (bname,bcity,offset,limit))
   records = cursor.fetchall()
   df = pd.DataFrame(records)
   df.columns = ['IFSC','BANK_ID','BRANCH','ADDRESS','CITY','DISTRICT','STATE','BANK_NAME']

   return jsonify(df.to_dict(orient= 'records'))

if __name__ == '__main__':
   app.run(debug=True)