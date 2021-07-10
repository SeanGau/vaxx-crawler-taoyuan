from flask import Flask
from flask_cors import CORS, cross_origin
import requests, re, json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def alert(message, redir): #alert then redirect
	return f'''<script type="text/javascript">
						alert("{message}");
						window.location.href = "{redir}";
						</script>'''

@app.route("/")
def home():
    return "<a href='/vaxx-taoyuan'>桃園疫苗施打資料</a>"
@app.route("/vaxx-taoyuan")
@cross_origin()
def vaxx_taoyuan():
    with open("static/datas/vaxx_taoyuan.json", encoding="utf-8") as json_file:
        return json_file.read()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)