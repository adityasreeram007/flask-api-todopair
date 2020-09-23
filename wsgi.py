from flask  import Flask,jsonify,request
import pandas
from flask_cors import CORS
import datetime
import sqlite3
import os.path
app=Flask(__name__)
CORS(app)

@app.route('/login',methods=['POST'])
def sender():
    data=pandas.read_csv('auth.csv')
    uname=list(data['Username'])
    upass=list(data['Password'])
    uteams=list(data['Teamname'])    
    ret={'status':'False','Team':'False'}
    datas=request.get_json()
    print(datas)
    use=datas['usename']
    passer=datas['pass']
    print(use,passer)
    if use in uname:
        i=uname.index(use)
        if upass[i]==passer:
            ret['status']=True
            ret['Team']=uteams[i]
     
    return ret
@app.route('/getdata',methods=['POST'])
def senddata():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "event_db.db")
    conn=sqlite3.connect(db_path)
    retdata={'data':None}
    datas=request.get_json()
    print(datas)
    teamname=datas['teamname']
    retarr=[]
    param=(str(teamname),)
    cur=conn.execute("select * from events where team=?",param)
    for row in cur:
        c=[]
        for j in row:
            c.append(j)
        retarr.append(c)
    # print(retarr)
    conn.commit()
    retdata['data']=retarr
    return retdata
@app.route('/putdata',methods=['POST'])
def putdata():
    
    resdata={'status':True}
    datas=request.get_json()
    temp=str(datetime.datetime.now())
    temp1=temp.split()
    temp1=temp1[::-1]
    temp1[0:2]=temp1[0:2][::-1]
    temp1[3:5]=temp1[3:5][::-1]
    temp1[6:]=temp1[6:][::-1]
    now=str(temp1[0]+","+temp1[1][0:8])
    values=(str(datas['team']), str(datas['title']), str(datas['desc']),str(now),str(datas['user']),)
    print(values)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "event_db.db")
    conn=sqlite3.connect(db_path)
    cur=conn.execute("insert into events values (?,?,?,?,?)",values)
    print(cur)
    conn.commit()
    return resdata    
    
if __name__ == '__main__':
    app.run(debug=True)