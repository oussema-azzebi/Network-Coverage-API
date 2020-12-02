# Network-Coverage-API
 API that retrieves 2G / 3G / 4G network coverage for each operator for each given address

## 1/ Install and start the app

- Clone the repo:

		git clone https://github.com/oussema-azzebi/Network-Coverage-API.git

- Go inside the repo :

		cd Network-Coverage-API/

- Create and activate virtual env:

		virtualenv env -p python3
		source env/bin/activate

- Install dependencies:

		pip3 install -r requirements.txt

- Run the server:

		python3 run.py

- An example of using the API:

GET: operator/?adress=1+avenue+claude+vellefaux+75010+paris

(http://127.0.0.1:5000/operator/?adress=1+avenue+claude+vellefaux+75010+paris)

The API should return:

{
  "Bouygue": {
    "2G": "True", 
    "3G": "True", 
    "4G": "True"
  }, 
  "Free": {
    "2G": "False", 
    "3G": "True", 
    "4G": "True"
  }, 
  "Orange": {
    "2G": "False", 
    "3G": "False", 
    "4G": "False"
  }, 
  "SFR": {
    "2G": "True", 
    "3G": "True", 
    "4G": "True"
  }
}


## 2/ Brief explanation of how the application works::

When launching the run.py script and strictly before starting the server, the start () method
is responsible for checking if the file "operator.csv" exists in api / data.

- Case where the "operator.csv" file exists:

We will use the searsh API "https://api-adresse.data.gouv.fr/search/" first to retrieve the name
of city for the desired address, and of the "operator.csv" file secondly in order to retrieve the
eligibility for each telephone operator for the desired address.
 
- Case where the "operator.csv" file does not exist:
  
If the file does not exist, we call the process_file() method in order to create it.

The process_file() method and from the file "2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"
will calculate the latitude and the logitude for each X and Y which will be used to retrieve the city name by using
of the reverse csv API "https://api-adresse.data.gouv.fr/reverse/csv/"

The limit of the reverse csv API is that it can no longer support a file with too many lines (> 70,000 lines)
and from about 30,000 lines it crashes and returns an error.
So the idea is to split the file we are going to send to the API. In the current case, we create 8 csv files 
and requesting the API each time to retrieve the name of the city for each latitude and longitude point.

We note the "significant" time that this operation takes to recover all the cities (3, 4 minutes)

At the end of this processing, we will have calculated all the names of the cities for each line in the file
We save in the api/data directory an "operator.csv" file with lat, lon, city as additional columns.
The process_file () method returns 1 if this process succeeds otherwise None.

Note: The application is delivered with the "operator.csv" file because the processing is already done offline
but you can try to delete it and run the script to see the creation of this file afterwards.

