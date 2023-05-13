from datetime import datetime
import time

import csv
import pprint

import responses

import requests

import googlemaps



# csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
# cal_cities = []
# state=", CA, USA"
# with open(csv_file_path, 'r') as file:
#     csvreader=csv.reader(file)
#     for row in csvreader:
# 	    cal_cities.append(row[1]+state)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(cal_cities)

class DistanceMatrixTest():


    def setUp(self):
        csv_file_path='/Users/huntervoid/programming/Ranking cities in NorCal/cal_cities.csv'
        cal_cities = []
        state=", USA"
        with open(csv_file_path, 'r') as file:
            csvreader=csv.reader(file)
            for row in csvreader:
    	        cal_cities.append(row[1]+state)	
        self.key = "AIzaSyAjE6UiHJdgkgDLJ5zDM2upMuX81b15WZI"
        self.client = googlemaps.Client(self.key)
        self.cal_cities = cal_cities
        # print(cal_cities)

        self.attractive_centers = [
			"San Francisco, USA"
			# "Berkeley, USA",
			# "Sacramento, USA"
			# "Napa",
			# "Sonoma",
			# "San Mateo",
			# "Palo Alto"
		]
        # self.attractive_centers = attractive_centers
    @responses.activate
    def test_basic_params(self):
        # responses.add(
        #     responses.GET,
        #     "https://maps.googleapis.com/maps/api/distancematrix/json",
        #     # body='{"status":"OK","rows":[]}',
        #     status=200,
        #     content_type="application/json",
        #     # stream=True
        # )

        responses.add(
            responses.GET,
            responses.calls[0].request.url,
            # body='{"status":"OK","rows":[]}',
            # status=200,
            content_type="application/json",
            # stream=True
        )

        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(responses)

        # pp.pprint(self.cal_cities)
        origins = self.cal_cities
        # pp.pprint(self.attractive_centers)
        destinations = self.attractive_centers
        # pp.pprint(destinations)

        matrix = self.client.distance_matrix(self.cal_cities[1:20], self.attractive_centers)

        # pp.pprint(matrix)
        # pp.pprint(responses.calls[0].request.url)

        

        payload={}
        headers={}
        pp.pprint(responses.calls[0].request.url)
        r = requests.request("GET", responses.calls[0].request.url)
        # r_json = r.json()
        pp.pprint(r)


        # pp.pprint(responses.rows[0])
        

        # r = requests.get(responses.calls[0].request.url)
        # pp.pprint(r.content)
        # for key in r:
    	#     pp.pprint( key)


foo = DistanceMatrixTest()
foo.setUp()
foo.test_basic_params()
