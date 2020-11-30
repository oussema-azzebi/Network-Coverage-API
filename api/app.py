from flask import Flask, request, jsonify, abort
from api.data.create_operator_file import process_file
import pathlib
import os
import requests
import json
import pandas as pd

app = Flask(__name__)

from api.errors import *

# Config options
app.config.from_object('config')

base_url_api_search = "https://api-adresse.data.gouv.fr/search/"

input_file = os.getcwd() + "/api/data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
output_file = os.getcwd() + "/api/data/operator.csv"
df_chunk_file = os.getcwd() + "/api/data/dataframe.csv"

operators_id = {"20801": "Orange",
				"20810": "SFR",
				"20815": "Free",
				"20820": "Bouygue"        
			} 

def get_operators(city):
	result = {}
	df = pd.read_csv(output_file, sep = ';')

	#filter by city
	df = df.loc[df['city'] == city]

	if 0 == len(df):
		msg = "No operator data available in our database for the requested address!"
		return jsonify(message = msg)
	else:
		for index in df.index:
			operateur = df['Operateur'][index]
			operateur_name = operators_id[str(operateur)]
			two_G = 'True' if df['2G'][index] == 1 else 'False'
			tree_G = 'True' if df['3G'][index] == 1 else 'False'
			four_G = 'True' if df['4G'][index] == 1 else 'False'
			result[operateur_name] = {"2G": two_G, "3G": tree_G, "4G": four_G}

		return result

def check_file_location(file_path):
	p = pathlib.Path(file_path)
	if p.is_file():
		#if file exist but empty, remove it and call again start method
		if os.stat(file_path).st_size == 0:
			os.remove(file_path)
			start()
		else:	
			return True
	else:
		return False

def start():
	"""Start method is called before flask application is started but strictly before the first request"""
	if check_file_location(output_file):
		pass 
	else:
		result = process_file(input_file, output_file, df_chunk_file)
		if result != 1:
			raise ("Error ! Cannot generate file")

@app.route("/operator/", methods=["GET"])
def listing_operators():
	adress = request.args.get('adress')
	if 0 == len(adress):
		msg = "No address has been entered..."
		return jsonify(message = msg)

	#get response from API search
	response = requests.get(base_url_api_search + '?q=' + adress)

	if response.status_code != 200:
		abort(404, description="Resource not found")
	try:
		content = json.loads(response.content.decode('utf-8'))
	except Exception as e:
		abort(500, description="Internal error")

	if 0 == len(content["features"]):
		msg = "No result for the address provided. Please enter a valid address !"
		return jsonify(message = msg)

	cities = []
	for feature in content["features"]:
		cities.append(feature["properties"]["city"])

	if len(set(cities)) > 2:
		msg = "Several cities have been found. Please specify your address !"
		return jsonify(message = msg)

	result = get_operators(cities[0])
	return jsonify(result)
