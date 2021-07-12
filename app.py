from flask import Flask, request
from flask_cors import CORS, cross_origin

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
    file_type = request.args.get("filetype", "csv")
    if file_type is "csv":
        with open("static/datas/vaxx_taoyuan.csv", encoding="utf-8-sig") as csv_file:
            return csv_file.read()
    else:
        with open("static/datas/vaxx_taoyuan.json", encoding="utf-8") as json_file:
            return json_file.read()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)