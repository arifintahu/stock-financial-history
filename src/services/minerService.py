from services.modules.helper import run_mining
from io import StringIO

def downloadFile(stock_code):
	textStream = StringIO();
	df = run_mining(stock_code)
	df.to_csv(textStream, index=False)
	return textStream.getvalue()