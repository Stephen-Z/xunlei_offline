# _*_ coding:UTF-8 _*_
from flask import Flask
from flask import request
from offlineapi import *

offline=Offline()
app=Flask(__name__)
@app.route('/api/taskcommit',methods=['POST'])
def commit_response():
    downloadurl=request.form['downloadurl']
    verifycode=request.form['verifycode']
    offline.taskcheck(downloadurl)
    if(offline.check_resultlist==['']):
        return 'downloadurl error'
    else:
        commitresult=offline.taskcommit(downloadurl,verifycode)
    if(commitresult[0]!='1'):
        return 'commit failure.please retry'
    else:
        return offline.getofflineurl(commitresult[1])




@app.route('/api/verifycode')
def code_response():
    if(os.path.exists('/zyh/js/verifycode1.png')):
        os.remove('verifycode1.png')
        picname=offline.getverifycode()
    else:
        if(os.path.exists('/zyh/js/verifycode2.png')):
            os.remove('verifycode2.png')
            picname=offline.getverifycode()
    return picname











if __name__ == "__main__":
	app.run(debug=True, host='127.0.0.1', port=5001)
