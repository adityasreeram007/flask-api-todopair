from flask  import Flask,jsonify,request
import pandas

data=pandas.read_csv('auth.csv')
uname=list(data['Username'])
upass=list(data['Password'])
uteams=list(data['Teamname'])

app=Flask(__name__)
@app.route('/login',methods=['POST'])
def sender():
    ret={'status':'False','Team':'False'}
    datas=request.form
    use=datas['username']
    passer=datas['password']
    print(use,passer)
    if use in uname:
        i=uname.index(use)
        if upass[i]==passer:
            ret['status']=True
            ret['Team']=uteams[i]
    
    return ret

    
if __name__ == '__main__':
    app.run(debug=True)