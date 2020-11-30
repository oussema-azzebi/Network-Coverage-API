# Network-Coverage-API
 API that retrieves 2G / 3G / 4G network coverage for each operator for each given address


- Clone the project 

- Create virtual env:

 	virtualenv env -p python3
	source env/bin/activate

- Install dependencies

        pip3 install -r requirements.txt

- Run the server

	python3 run.py

- An example of using the API :

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
