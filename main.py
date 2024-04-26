from flask import Flask, render_template, url_for ,redirect, request
import json
import sqlite3
from datetime import datetime,timedelta


app = Flask(__name__)

 
@app.route('/')
def home():
    #fetch data from the google sheet
    condition = False
    if():
        condition = True
    return render_template('home.html',condition = True
    
    
    
    )


def is_table_exists(table_name):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()

    conn.close()

    return result is not None

def is_table_exists_appointmentdb(table_name):
    conn = sqlite3.connect('appointment.db')  
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cursor.fetchone()

    conn.close()

    return result is not None






@app.route('/doctor_login', methods = ['GET','POST'])
def doctor_login():
    if request.method == 'POST':
        if (is_table_exists("DoctorLogin") == True):
            userid = request.form['userid']
            password = request.form['password']
            status = request.form['status']
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            query = "select * from DoctorLogin where  userid = ?"
            cursor.execute(query, (userid,))
            result = cursor.fetchone()
            print(result)
            
            if result == None :
                return render_template("doctor_login.html" , message = "Invalid Username")

            elif  result[1] == password:
                print("ok")
                query = "insert into DoctorStatus(userid, status, time) values(?,?,?)"
                cursor.execute(query,(userid,status,datetime.now()))
                connection.commit()
                cursor.close()
                connection.close()
                print("before doctor dashboard")
                return redirect(url_for("doctor_dashboard"))
            else:
                return render_template("doctor_login.html",message = "Incorrect password")
            

        else:
            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()
            query = 'Create table DoctorLogin(userid varchar(50) PRIMARY KEY, password varchar(50) );'
            cursor.execute(query)

            query = 'Create table DoctorStatus(userid varchar(50), status varchar(10), time DATETIME DEFAULT CURRENT_TIMESTAMP);'
            cursor.execute(query)

            query = "insert into DoctorLogin(userid, password) values('22it31','britto123');"
            cursor.execute(query)
            connection.commit()

            

            cursor.close()
            connection.close()
            return render_template("doctor_login.html")
    
    return render_template("doctor_login.html")


    
@app.route('/doctor_loginform')
def doctor_loginform():
    return render_template("doctor_login.html")


@app.route('/doctor_dashboard')
def doctor_dashboard():
    print("inside doctor_dashboard")
    connection = sqlite3.connect("appointment.db")
    cursor = connection.cursor()
    query = "select * from Appointments where time > ?"
    cursor.execute(query, (datetime.now(),))
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("doctor_dashboard.html",data = result)



@app.route('/appointments')
def appointments():
    if is_table_exists_appointmentdb("Appointments"):
        print("inside selection appointments")
        conn = sqlite3.connect("appointment.db")
        cursor = conn.cursor()
        query = "select appno from Appointments ORDER BY appno DESC LIMIT 1"
        cursor.execute(query)
        appno = cursor.fetchone()
        appno = appno[0] + 1

        query = "select time from Appointments ORDER BY time DESC LIMIT 1"
        cursor.execute(query)
        time = cursor.fetchone() 
        date_string_intable = time[0]#select the last encountered time 
        current_datetime = datetime.now()
        date_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
        # last_app_time = date_time_obj.time()
        # current_time = datetime.now().time()
        delta = timedelta(minutes=15)
        new_date_time_obj = date_time_obj + delta
        apptime = new_date_time_obj.time()
        # new_date_string = new_date_time_obj.strftime('%Y-%m-%d %H:%M:%S.%f')

        return render_template("appointment.html",appno = appno , apptime = apptime)
    
    
    else:
        print("inside create appointment")
        connection = sqlite3.connect("appointment.db")
        cursor = connection.cursor()
        query = "Create table Appointments(appno int primary key,doctor varchar(50),name varchar(25), age int, weight int, symptom varchar(300),time DATETIME DEFAULT CURRENT_TIMESTAMP)"
        cursor.execute(query)


        query = "insert into Appointments(appno,doctor,name,age,weight,symptom,time) values(?,?,?,?,?,?,?) "
        value = (0,"-","-",0,0,"-",datetime.now())
        cursor.execute(query,value)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('appointments'))



@app.route('/appointments_patient', methods = ['GET', 'POST'])
def appointments_patient():
    if request.method == 'POST':
        if (is_table_exists_appointmentdb("Appointments") == True):
            name = request.form['name']
            age = int(request.form['age'])
            weight = int(request.form['weight'])
            symptom = request.form['symptoms']
            doctor = "doctor_1"
            connection = sqlite3.connect("appointment.db")
            cursor = connection.cursor()
            query = "select appno from Appointments ORDER BY appno DESC LIMIT 1 "
            cursor.execute(query)
            last_appno = cursor.fetchone()

            query = "select time from Appointments ORDER BY time DESC LIMIT 1"
            cursor.execute(query)
            last_app_time = cursor.fetchone()#last time in database
            date_string = last_app_time[0]

            #app_date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
            # delta = timedelta(minutes=15)
            # new_date_time_obj = date_time_obj + delta
            # new_date_string = new_date_time_obj.strftime('%Y-%m-%d %H:%M:%S.%f')  

            current_datetime = datetime.now()
            date_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')#string
            date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
            
            delta = timedelta(minutes=15)
            last_appnotime = date_time_obj + delta
            

            if last_appno :
                appno = int(last_appno[0] + 1)
                
                if appno <= 10:
                    query = "insert into Appointments(appno,doctor,name,age,weight,symptom,time) values(?,?,?,?,?,?,?)"
                    cursor.execute(query,(appno,doctor,name,age,weight,symptom,last_appnotime))
                    print("Before commit")
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return redirect(url_for('myappointments'))
                else :
                    return render_template("full.html")
            else :
                return 0

        

    return render_template("appointment.html")



@app.route("/myappointments")
def myappointments():
    connection = sqlite3.connect("appointment.db")
    cursor = connection.cursor()
    query = "select * from Appointments"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("myappointments.html" , data=result)


#for check up 
@app.route("/hi")
def summa():
    connection = sqlite3.connect("appointment.db")
    cursor = connection.cursor()
    query = "select * from Appointments"
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    connection.close()
    return "ok"


if '__main__' == __name__ :
    app.run()