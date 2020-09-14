from flask  import Flask,jsonify
import pandas
data=pandas.read_csv('auth.csv')
uname=list(data['Username'])
upass=list(data['Password'])
uteams=list(data['Teamname'])

app=Flask(__name__)
@app.route('/<par>',methods=['GET'])
def sender(par):
    ret={'status':'False','Team':'False'}
    cred=par.split('&')
    print(cred[0].split('=')[1])
    if cred[0].split('=')[1] in uname:
        ind=uname.index(cred[0].split('=')[1])
        if upass[ind]==cred[1].split('=')[1]:
            ret['status']='True'
            ret['Team']=uteams[ind]
    print(par)
    return jsonify(ret)

    
if __name__ == '__main__':
    app.run(debug=True)