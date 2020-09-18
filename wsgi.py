from flask  import Flask,jsonify,request
import pandas
from flask_cors import CORS

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
    return jsonify(retdata)
    
    
    
    
    
if __name__ == '__main__':
    app.run(debug=True)