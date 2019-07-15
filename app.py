from flask import Flask, render_template, url_for, request, jsonify, flash
from wtforms import Form, StringField, IntegerField, validators, SelectField
import urllib3, json, requests, calendar
import pymysql
from flaskext.mysql import MySQL
import os

db = pymysql.connect("localhost","root","ahmed@12345","farmula_dashboard")

app = Flask(__name__)
 
# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'yfarm'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL()
# mysql.init_app(app)

#IBM Watson Credenials 
wml_credentials={
    "url":'https://eu-gb.ml.cloud.ibm.com',
    "username": '461336f2-8984-492a-b72a-9376b8e9d1c2',
    "password": 'de3136e2-2a65-48cd-85f7-77dd03715ba3'
    }

#init header and request and getting response 
headers = urllib3.util.make_headers(basic_auth='{username}:{password}'.format(username=wml_credentials['username'], password=wml_credentials['password']))
url = '{}/v3/identity/token'.format(wml_credentials['url'])
response = requests.get(url, headers=headers)
mltoken = json.loads(response.text).get('token')

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

class PredicitForm(Form):
    month = SelectField(u'Pick a Month', choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'Novmber'), ('12', 'December')])
    year = IntegerField(u'Enter a Year', [validators.NumberRange(min=1970, max=2050)])

@app.route('/cocoyam', methods=['GET','POST'])
def cocoyam():

    cursor = db.cursor()
    cursor.execute("SELECT  * FROM  prediction where crop = 'Cocoyam'")
    data = cursor.fetchall()
    print(data)
    cursor.close()

    form = PredicitForm(request.form)
    if request.method == 'POST' and form.validate():
        month = form.month.data
        year = form.year.data
        payload_scoring = {"fields":["MONTH","YEAR"],"values":[[int(month),year]]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/1d441776-58fb-4e22-8975-aa9b1c4a40a9/online', json=payload_scoring, headers=header)
        print("Scoring response")
        print(json.loads(response_scoring.text)) 
        print(month)
        response = json.loads(response_scoring.text)

        #get result from the response 
        month_num = int(response['values'][0][0])
        month_i = "Month : " + calendar.month_name[month_num]
        year =  "Year : " + str(response['values'][0][1])
        pre_prams = str(response['values'][0][2])
        price_round = ("%.2f" % round(response['values'][0][3],2))
        price = str("Predict Price :  "+ price_round + " GHS (250KG)")
        return render_template('cocoyam.html', form=form, month_i=month_i, year=year, price=price)

    
    
    return render_template('cocoyam.html', form=form , data=data)     


@app.route('/maize', methods=['GET','POST'])
def maize():

    cursor = db.cursor()
    cursor.execute("SELECT  * FROM  prediction where crop = 'Maize' ")
    data = cursor.fetchall()
    print(data)
    cursor.close()

    form = PredicitForm(request.form)
    if request.method == 'POST' and form.validate():
        month = form.month.data
        year = form.year.data
        payload_scoring = {"fields":["Year","Month"],"values":[[year,int(month)]]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/eee31a61-23bb-436e-a5b4-8b7e8a020bec/online', json=payload_scoring, headers=header)
        print("Scoring response")
        print(json.loads(response_scoring.text)) 
        print(month)
        response = json.loads(response_scoring.text)

        #get result from the response 
        month_num = int(response['values'][0][1])
        month_i = "Month : " + calendar.month_name[month_num]
        year =  "Year : " + str(response['values'][0][0])
        pre_prams = str(response['values'][0][2])
        price_round = ("%.2f" % round(response['values'][0][3],2))
        price = str("Predict Price :  "+ price_round + " GHS (100KG)")
        return render_template('maize.html', form=form, month_i=month_i, year=year, price=price, data=data)

    
    
    return render_template('maize.html', form=form , data=data)

@app.route('/millet', methods=['GET','POST'])
def millet():

    cursor = db.cursor()
    cursor.execute("SELECT  * FROM  prediction where crop = 'Millet' ")
    data = cursor.fetchall()
    print(data)
    cursor.close()

    form = PredicitForm(request.form)
    if request.method == 'POST' and form.validate():
        month = form.month.data
        year = form.year.data
        payload_scoring = {"fields":["Year","Month"],"values":[[year,int(month)]]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/38f26f63-b3a7-4a2b-b405-c4acddf5f906/online', json=payload_scoring, headers=header)
        print("Scoring response")
        print(json.loads(response_scoring.text)) 
        print(month)
        response = json.loads(response_scoring.text)

        #get result from the response 
        month_num = int(response['values'][0][1])
        month_i = "Month : " + calendar.month_name[month_num]
        year =  "Year : " + str(response['values'][0][0])
        pre_prams = str(response['values'][0][2])
        price_round = ("%.2f" % round(response['values'][0][3],2))
        price = str("Predict Price :  "+ price_round + " GHS (93KG)")
        return render_template('millet.html', form=form, month_i=month_i, year=year, price=price, data=data)

    
    
    return render_template('millet.html', form=form , data=data) 


@app.route('/sorghum', methods=['GET','POST'])
def sorghum():

    cursor = db.cursor()
    cursor.execute("SELECT  * FROM  prediction where crop = 'Sorghum' ")
    data = cursor.fetchall()
    print(data)
    cursor.close()

    form = PredicitForm(request.form)
    if request.method == 'POST' and form.validate():
        month = form.month.data
        year = form.year.data
        payload_scoring = {"fields":["Year","Month"],"values":[[year,int(month)]]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/62f973dd-c8a8-4c80-bce3-022b9475d7b5/online', json=payload_scoring, headers=header)
        print("Scoring response")
        print(json.loads(response_scoring.text)) 
        print(month)
        response = json.loads(response_scoring.text)

        #get result from the response 
        month_num = int(response['values'][0][1])
        month_i = "Month : " + calendar.month_name[month_num]
        year =  "Year : " + str(response['values'][0][0])
        pre_prams = str(response['values'][0][2])
        price_round = ("%.2f" % round(response['values'][0][3],2))
        price = str("Predict Price :  "+ price_round + " GHS (250KG)")
        return render_template('sorghum.html', form=form, month_i=month_i, year=year, price=price, data=data)

    
    
    return render_template('sorghum.html', form=form , data=data) 



@app.route('/rice', methods=['GET','POST'])
def rice():
    cursor = db.cursor()
    cursor.execute("SELECT  * FROM  prediction where crop = 'Rice' ")
    data = cursor.fetchall()
    print(data)
    cursor.close()

    form = PredicitForm(request.form)
    if request.method == 'POST' and form.validate():
        month = form.month.data
        year = form.year.data
        payload_scoring = {"fields":["Year","Month"],"values":[[year,int(month)]]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/ac8f4cbf-a774-49f2-944c-6d8afe756b99/online', json=payload_scoring, headers=header)
        print("Scoring response")
        print(json.loads(response_scoring.text)) 
        print(month)
        response = json.loads(response_scoring.text)

        #get result from the response 
        month_num = int(response['values'][0][1])
        month_i = "Month : " + calendar.month_name[month_num]
        year =  "Year : " + str(response['values'][0][0])
        pre_prams = str(response['values'][0][2])
        price_round = ("%.2f" % round(response['values'][0][3],2))
        price = str("Predict Price :  "+ price_round + " GHS (100KG)")
        return render_template('rice.html', form=form, month_i=month_i, year=year, price=price, data=data)

    
    
    return render_template('rice.html', form=form , data=data) 


@app.route('/yam', methods=['GET','POST'])
def yam():
    cursor = db.cursor()
    cursor.execute("SELECT  * FROM  prediction where crop = 'Yam' ")
    data = cursor.fetchall()
    print(data)
    cursor.close()

    form = PredicitForm(request.form)
    if request.method == 'POST' and form.validate():
        month = form.month.data
        year = form.year.data
        payload_scoring = {"fields":["MONTH","YEAR"],"values":[[int(month),year]]}
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v3/wml_instances/6a216236-adcc-48b5-901f-41e4cafbf033/deployments/1d441776-58fb-4e22-8975-aa9b1c4a40a9/online', json=payload_scoring, headers=header)
        print("Scoring response")
        print(json.loads(response_scoring.text)) 
        print(month)
        response = json.loads(response_scoring.text)

        #get result from the response 
        month_num = int(response['values'][0][0])
        month_i = "Month : " + calendar.month_name[month_num]
        year =  "Year : " + str(response['values'][0][1])
        pre_prams = str(response['values'][0][2])
        price_round = ("%.2f" % round(response['values'][0][3],2))
        price = str("Predict Price :  "+ price_round + " GHS (250KG)")
        return render_template('yam.html', form=form, month_i=month_i, year=year, price=price, data=data)

    
    
    return render_template('yam.html', form=form , data=data)  

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(host='0.0.0.0')