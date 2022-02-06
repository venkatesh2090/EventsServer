from flask import Flask, Response

app = Flask(__name__)

@app.route('/webex/callback', methods=['POST'])
def webex_callback():
    print('hello World')
    return Response(None, 201)