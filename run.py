from api.app import app, start
import os

#input_file = os.getcwd() + "/api/data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
#output_file = os.getcwd() + "/api/data/operator.csv"
#df_chunk_file = os.getcwd() + "/api/data/dataframe.csv"

if __name__ == "__main__":
	#start(input_file, output_file, df_chunk_file)
	start()
	app.run(debug=True)
