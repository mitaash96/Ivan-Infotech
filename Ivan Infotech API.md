# Flask API: Indian Banks

## Imports


```python
from flask import *
from flaskext.mysql import MySQL
import pandas as pd
```

## Initializing Flask app


```python
app = Flask(__name__)
```

## Establish connection to MYSQL, Localhost


```python
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'mitaash'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Pmitaash_2607'
app.config['MYSQL_DATABASE_DB'] = 'sql_invoicing'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
```


```python
conn = mysql.connect()
cursor =conn.cursor()
```

## Building URLs:

### Default page http://127.0.0.1:5000


```python
@app.route('/')
def default1():
   dictmanual = {"Default":"http://127.0.0.1:5000/",
   "By_IFSC":"http://127.0.0.1:5000/bank_ifsc/<ifsc>/<offset>/<limit>",
   "By_BANKNAME_CITY":"http://127.0.0.1:5000/bank_name_city/<bname>/<bcity>/<offset>/<limit>",}

   return jsonify(dictmanual)
```

### Search by IFSC:

format: ../bank_ifsc/(ifsc code)/(offset)/(limit)

example: ../bank_ifsc/ABHY0065001/0/1


```python
@app.route('/bank_ifsc/<ifsc>/<int:offset>/<int:limit>', methods = ["GET"])
def func1(ifsc,offset,limit):

   if offset>0: offset = 0

   sql_query = """ SELECT * FROM branches WHERE ifsc = %s LIMIT %s , %s """
   cursor.execute(sql_query, (ifsc,offset,limit))
   records = cursor.fetchall()
   df = pd.DataFrame(records)
   df.columns = ['IFSC','BANK_ID','BRANCH','ADDRESS','CITY','DISTRICT','STATE','BANK_NAME']

   return jsonify(df.to_dict(orient= 'records'))
```

### Search by bank name and city:

format:../bank_name_city/(bank name)/(city)/(int:offset)/(int:limit)

example:../bank_name_city/ABHYUDAYA%20COOPERATIVE%20BANK%20LIMITED/MUMBAI/0/3


```python
@app.route('/bank_name_city/<bname>/<bcity>/<int:offset>/<int:limit>', methods = ["GET"])
def func2(bname, bcity,offset,limit):

   sql_query = """ SELECT * FROM branches WHERE bank_name = %s AND city = %s LIMIT %s , %s """
   cursor.execute(sql_query, (bname,bcity,offset,limit))
   records = cursor.fetchall()
   df = pd.DataFrame(records)
   df.columns = ['IFSC','BANK_ID','BRANCH','ADDRESS','CITY','DISTRICT','STATE','BANK_NAME']

   return jsonify(df.to_dict(orient= 'records'))
```

## App.run()


```python
if __name__ == '__main__':
   app.run(debug=True)
```
