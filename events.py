from urllib import response
from flask import Flask, Response, request, json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

@app.route('/webex/callback', methods=['GET','POST'])
def webex_callback():
    if request.method == 'POST':
        reqData = json.loads(response.json)
        print(reqData.data.id)
        print(reqData.data.personEmail)
        return Response('OK', 200)
    else:
        return Response("I'm alive", 200)