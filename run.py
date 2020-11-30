from api.app import app, start
import os

if __name__ == "__main__":
	start()
	app.run(debug=True)
