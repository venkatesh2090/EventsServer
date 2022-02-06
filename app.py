from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/webex/callback', methods=['GET','POST'])
def webex_callback():
    if request.method == 'POST':
        print(request.json)
        print('hello World')
        return Response(None, 200)
    else:
        return Response("I'm alive", 200)