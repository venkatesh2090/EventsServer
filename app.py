from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/webex/callback', methods=['POST'])
def webex_callback():
    print(request.json)
    print('hello World')
    return Response(None, 200)