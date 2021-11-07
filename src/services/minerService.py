from src.services.modules.helper import run_mining
from io import StringIO

def downloadFile(stock_code, security_code, username):
	textStream = StringIO();
	df = run_mining(stock_code, security_code, username)
	df.to_csv(textStream, index=False)
	return textStream.getvalue()