from flask import Flask, Response

app = Flask(__name__)

@app.route('/webex/callback', methods=['POST'])
def webex_callback():
    return Response(None, 201)