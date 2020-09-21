from flask  import Flask,jsonify,request
import pandas
from flask_cors import CORS
import datetime
import csv
data=None
uname=None
upass=None
uteams=None
eventdata=None
eteams=None
ename=None
edesc=None
etime=None
eby=None
def readdata():
    global data,uname,upass,uteams,eventdata,eteams,ename,edesc,etime,eby
    data=pandas.read_csv('auth.csv')
    uname=list(data['Username'])
    upass=list(data['Password'])
    uteams=list(data['Teamname'])
    eventdata=pandas.read_csv('eventlist.csv')
    eteams=list(eventdata['team'])
    ename=list(eventdata['event_name'])
    edesc=list(eventdata['description'])
    etime=list(eventdata['time'])
    eby=list(eventdata['by'])
    
readdata()
app=Flask(__name__)
CORS(app)
@app.route('/login',methods=['POST'])
def sender():
    
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
    
    retdata={'data':None}
    datas=request.get_json()
    print(datas)
    teamname=datas['teamname']
    retarr=[]
    for i in range(len(eteams)):
        arr=[]
        if eteams[i]==teamname:
            arr.append(ename[i])
            arr.append(edesc[i])
            arr.append(etime[i])
            arr.append(eby[i])
            retarr.append(arr)
    retdata['data']=retarr
    # print(retdata)        
    return retdata
@app.route('/putdata',methods=['POST'])
def putdata():
    
    resdata={'status':False}
    datas=request.get_json()
    temp=str(datetime.datetime.now())
    temp1=temp.split()
    now=str(temp1[0][::-1]+","+temp1[1][0:8])
    
    with open('eventlist.csv', 'a+',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datas['team'], datas['title'], datas['desc'],now,datas['user']])
        resdata['status']=True
        
        file.close()
        
    readdata()
    return resdata    
    
if __name__ == '__main__':
    app.run(debug=True)