from flask import jsonify
from api.app import app

@app.errorhandler(404)
def resource_not_found(e):
	return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(e):
	return jsonify(error=str(e)), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

