from flask import Flask
from data.create_operator_file import process_file

app = Flask(__name__)

# Config options
app.config.from_object('config')

@app.route('/')
def index():
	return "Hello world !"

if __name__ == "__main__":
	app.run()