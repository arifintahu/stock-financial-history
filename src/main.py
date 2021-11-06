from flask import Flask, render_template, request, make_response
from src.services.minerService import downloadFile

class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string="%%",
		variable_end_string="%%",
	))

app = CustomFlask(__name__)

@app.route("/", methods=["GET"])
def index():
	if request.method == "GET":
		return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
	if request.method == "POST":
		body 			= request.get_json()
		stock_code 		= body['stock_code']
		security_code 	= body['security_code']
		username 		= body['username']
		csv_output 		= downloadFile(stock_code, security_code, username)
		resp 			= make_response(csv_output)
		resp.headers["Content-Disposition"] = ("attachment; filename=financial-history-%s.csv" % stock_code)
		resp.headers["Content-Type"] = "text/csv"
		return resp
	